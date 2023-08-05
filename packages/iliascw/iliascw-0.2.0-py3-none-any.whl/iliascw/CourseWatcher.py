from time import sleep
from bs4 import BeautifulSoup, Tag
import requests
from pydantic import BaseModel
from datetime import datetime
import bisect
import logging

from .Configuration import WatchConfig, IliasConfig, AvailabilityTask, UpdateTask
from .Result import CourseSnapshot, CourseResult, IliasListItem, IliasListItemDifference, UpdateResult, AvailabilityResult, CourseDiff, WatchResult

logger = logging.getLogger(__name__)

class Memory:

    def __init__(self):
        self._mem: dict[str, list[CourseSnapshot]] = {}

    def remember(self, snapshot: CourseSnapshot) -> None:
        bisect.insort(self._mem[snapshot.object_id], snapshot, key=lambda s: s.time)

    def get_latest(self, object_id: str) -> CourseSnapshot | None:
        try:
            return self._mem[object_id][-1]
        except KeyError or IndexError:
            return None

    def get_previous(self, object_id: str) -> CourseSnapshot | None:
        try:
            return self._mem[object_id][-2]
        except KeyError or IndexError:
            return None


class ConnectionError(Exception):
    pass

class ParseError(Exception):
    pass

class CourseWatcher:

    def __init__(self, ilias: IliasConfig, watchconf: WatchConfig, memory: Memory) -> None:
        self.ilias = ilias
        self.watchconf = watchconf
        self.session = requests.Session()
        self.memory = memory
        self.session = requests.Session()

    def _is_logged_in(self) -> bool:
        resp = self.session.get(self.ilias.domain)
        if resp.status_code != 200:
            raise ConnectionError(f'Failed to connect to the domain {self.ilias.domain}')
        return b'href="https://www.studon.fau.de/studon/login.php' in resp.content

    def _login(self):
        if self._is_logged_in():
            return
        self.session.post(
            'https://www.studon.fau.de/studon/ilias.php?lang=de&cmd=post&cmdClass=ilstartupgui&cmdNode=16d&baseClass=ilStartUpGUI&rtoken=',
            data={
                'username': self.ilias.username,
                'password': self.ilias.password,
                'cmd[doStandardAuthentication]': 'Anmelden'
            }
        )
        if not self._is_logged_in():
            logger.error("Failed to log in.")
            raise ConnectionError('Failed to log in.')

    def watch(self) -> WatchResult:
        course_results: dict[str, CourseResult] = {}

        def get_html_txt(obj: str) -> str:
            url = self.ilias.domain + '/' + obj + '.html'
            n = 5
            for i in range(n):
                self._login()
                resp: requests.Response = self.session.get(url)
                if resp.status_code not in [200, 302]:
                    logger.warning(f'Could not fetch "{url}". Status code: {resp.status_code} | Body: {resp.content}')
                    sleep(5)
                    continue
                return resp.text
            raise ConnectionError(f'Failed to fetch {url} after multiple {n} tries')

        for object_id, crsconf in self.watchconf.courses.items():
            html_resp = get_html_txt(object_id)
            soup = BeautifulSoup(html_resp, 'html.parser')
            items = soup.find_all('div', class_='il_ContainerListItem')

            listitems_list: list[IliasListItem] = []
            for item in items:
                list_item = IliasListItem(item)
                listitems_list.append(list_item)

            title = soup.find('a', {'id': 'il_mhead_t_focus'})
            if not isinstance(title, Tag):
                raise ParseError(f"Title for course with object id {object_id} is not a tag.")

            current = CourseSnapshot(object_id=object_id, title=title.text, items=listitems_list, time=datetime.now())
            self.memory.remember(current)

            crs_result = CourseResult(update=None, availability=[])

            current = self.memory.get_latest(object_id)
            previous = self.memory.get_previous(object_id)
            crsdiff: CourseDiff = CourseDiff(
                after=current,
                before=previous
            )

            if crsconf.update_task:
                crs_result.update = UpdateResult(failed=False, diff=crsdiff)

            for availability_task in crsconf.availability_tasks:
                availability_result = AvailabilityResult(failed=False, availables=crsdiff.search_matching_listitems(availability_task.search_string))
                crs_result.availability.append(
                    availability_result
                )

            course_results[object_id] = crs_result
        return WatchResult(courses=course_results)
