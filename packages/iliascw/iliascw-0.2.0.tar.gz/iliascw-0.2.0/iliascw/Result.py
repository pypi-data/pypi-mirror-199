from typing import Any

from pydantic import BaseModel
from datetime import datetime

class Result(BaseModel):
    failed: bool

class ItemTitle(BaseModel):
    text: str
    href: str

class ItemLocation(BaseModel):
    pass

class ItemAllLocation(ItemLocation):
    pass

class ItemTitleLocation(ItemLocation):
    pass

class ItemTitleTextLocation(ItemTitleLocation):
    pass

class ItemTitleHrefLocation(ItemTitleLocation):
    pass

class ItemDescriptionLocation(ItemLocation):
    pass

class ItemPropertyLenLocation(ItemLocation):
    pass

class ItemPropertyLocation(ItemLocation):
    def __init__(self, index):
        self.index = index

class IliasListItem(BaseModel):
    title: ItemTitle
    description: str
    properties: list[str]

    def __init__(self, list_item: Any) -> None:
        t = list_item.find('a', class_='il_ContainerItemTitle')
        self.title = ItemTitle(text=t.text, href=t.href)
        self.description = list_item.find('a', class_='il_Description')
        self.properties = [item_property.text for item_property in list_item.find_all('span', class_='il_ItemProperty')]

    def match_string(self, string: str) -> list[ItemLocation]:
        locations: list[ItemLocation] = []
        if string in self.title.text:
            locations.append(ItemTitleTextLocation())
        if string in self.title.href:
            locations.append(ItemTitleHrefLocation())
        if string in self.description:
            locations.append(ItemDescriptionLocation())
        for i, prop in enumerate(self.properties):
            if string in prop:
                locations.append(ItemPropertyLocation(i))
        return locations

class DifferenceEvent(BaseModel):
    locations: list[ItemLocation]

class AddEvent(DifferenceEvent):
    pass

class DeleteEvent(DifferenceEvent):
    pass

class ChangeEvent(DifferenceEvent):
    pass

class IliasListItemDifference(BaseModel):
    before: IliasListItem | None
    after: IliasListItem | None

    def __init__(self, before: IliasListItem | None, after: IliasListItem | None) -> None:
        self.before = before
        self.after = after

    def get_changes(self) -> list[DifferenceEvent]:
        if self.is_equal():
            return []

        if self.before is None and self.after is not None:
            return [AddEvent(locations=[ItemAllLocation()])]

        if self.before is not None and self.after is None:
            return [DeleteEvent(locations=[ItemAllLocation()])]

        # This should always be true because of the is_equal call at the start
        assert(self.before is not None and self.after is not None)

        change_locations: list[ItemLocation] = []

        if self.before.title.text != self.after.title.text:
            change_locations.append(ItemTitleTextLocation())
        if self.before.title.href != self.after.title.href:
            change_locations.append(ItemTitleHrefLocation())
        if self.before.description != self.after.description:
            change_locations.append(ItemDescriptionLocation())

        before_prop_n = len(self.before.properties)
        after_prop_n = len(self.after.properties)
        if before_prop_n != after_prop_n:
            change_locations.append(ItemPropertyLenLocation())
            return [ChangeEvent(locations=change_locations)]

        for i in range(before_prop_n):
            if self.before.properties[i] != self.after.properties[i]:
                change_locations.append(ItemPropertyLocation(index=i))
        return [ChangeEvent(locations=change_locations)]
        

    def match_string(self, string: str) -> list[DifferenceEvent]:
        if self.is_equal():
            return []

        if self.before is None and self.after is not None:
            add_locations = self.after.match_string(string)
            if len(add_locations) != 0:
                return [AddEvent(locations=add_locations)]
            return []

        if self.before is not None and self.after is None:
            delete_locations = self.before.match_string(string)
            if len(delete_locations) != 0:
                return [DeleteEvent(locations=delete_locations)]
            return []

        # This should always be true because of the is_equal call at the start
        assert(self.before is not None and self.after is not None)

        locations_before = self.before.match_string(string)
        locations_after = self.after.match_string(string)

        all_locations: set[ItemLocation] = set()
        all_locations.update(locations_before)
        all_locations.update(locations_after)

        change_locations: list[ItemLocation] = []
        add_locations: list[ItemLocation] = []
        delete_locations: list[ItemLocation] = []
        for location in all_locations:
            if location in locations_before and location in locations_after:
                change_locations.append(location)
                continue
            if location in locations_before:
                delete_locations.append(location)
            if location in locations_after:
                add_locations.append(location)

        events: list[DifferenceEvent] = []
        if len(change_locations) != 0:
            events.append(ChangeEvent(locations=change_locations))
        if len(add_locations) != 0:
            events.append(AddEvent(locations=add_locations))
        if len(delete_locations) != 0:
            events.append(DeleteEvent(locations=delete_locations))
        return events

    def is_equal(self) -> bool:
        return self.before == self.after

class CourseSnapshot(BaseModel):
    object_id: str
    title: str
    items: list[IliasListItem]
    time: datetime

class CourseDiff(BaseModel):
    title_change: tuple[str | None, str | None]
    itemchanges_by_title: dict[str, IliasListItemDifference]

    def __init__(self, before: CourseSnapshot | None, after: CourseSnapshot | None) -> None:
        def items_by_title(items: list[IliasListItem]) -> dict[str, IliasListItem]:
            return {item.title.text: item for item in items}

        changes: dict[str, IliasListItemDifference] = {}
        before_by_items = items_by_title(before.items) if before else {}
        after_by_items = items_by_title(after.items) if after else {}

        all_keys: set[str] = set()
        all_keys.update(before_by_items.keys())
        all_keys.update(after_by_items.keys())

        for title in all_keys:
            item_before = before_by_items.get(title)
            item_after = after_by_items.get(title)
            diff = IliasListItemDifference(before=item_before, after=item_after)
            if not diff.is_equal():
                changes[title] = diff

        self.itemchanges_by_title = changes
        title_change: list[str | None] = [None, None]
        if before:
            title_change[0] = before.title
        if after:
            title_change[1] = after.title
        self.title_change = tuple(title_change)

    def search_matching_listitems(self, search_string: str) -> dict[str, list[DifferenceEvent]]:
        matching_listitems: dict[str, list[DifferenceEvent]] = {}
        for title, change in self.itemchanges_by_title.items():
            match: list[DifferenceEvent] = change.match_string(search_string)
            if len(match):
                matching_listitems[title] = match
        return matching_listitems

class UpdateResult(Result):
    diff: CourseDiff

class AvailabilityResult(Result):
    availables: dict[str, list[DifferenceEvent]]

class CourseResult(BaseModel):
    update: UpdateResult | None
    availability: list[AvailabilityResult]

class WatchResult(BaseModel):
    courses: dict[str, CourseResult]

