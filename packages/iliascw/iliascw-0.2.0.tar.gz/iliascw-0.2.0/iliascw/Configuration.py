#!/usr/bin/env python3

from abc import abstractmethod
import os
from pydantic import BaseModel
import logging
import json

from .ConfigurationStrings import ConfigurationStrings as CS
from .IliasConfig import ILIAS_USERNAME, ILIAS_PASSWORD, ILIAS_DOMAIN

logger = logging.getLogger('uvicorn')

class Stakeholders(BaseModel):
    telegramNotifications: set[str]
    mailNotifications: set[str]

    def include(self, other: 'Stakeholders'):
        self.telegramNotifications = self.telegramNotifications.union(other.telegramNotifications)
        self.mailNotifications = self.mailNotifications.union(other.mailNotifications)

    def clear(self):
        self.telegramNotifications.clear()
        self.mailNotifications.clear()

class Task(BaseModel):
    stakeholders: Stakeholders

    @abstractmethod
    def merge_into_course(self, course: 'CourseConfig') -> None:
        raise NotImplementedError("virtual function")

class UpdateTask(Task):

    def merge_into_course(self, course: 'CourseConfig') -> None:
        if course.update_task is None:
            logger.debug("Matching update task was not found. Replacing with constructed update task.")
            course.update_task = self
        else:
            logger.debug("Matching update task was found. Including the new stakeholders in the current task.")
            course.update_task.stakeholders.include(self.stakeholders)

class AvailabilityTask(Task):
    search_string: str

    def merge_into_course(self, course: 'CourseConfig') -> None:
        found_course = None
        for availability_task in course.availability_tasks:
            if availability_task.search_string == self.search_string:
                found_course = availability_task
                break

        if found_course is None:
            logger.debug("Matching availability task was not found. Replacing with constructed availability task.")
            course.availability_tasks.append(self)
        else:
            logger.debug("Matching availability task was found. Including the new stakeholders in the current task.")
            found_course.stakeholders.include(self.stakeholders)

class CourseConfig(BaseModel):
    update_task: UpdateTask | None
    availability_tasks: list[AvailabilityTask]

class WatchConfig(BaseModel):
    courses: dict[str, CourseConfig]

    def register_task(self, object_id: str, task: Task) -> None:
        if object_id not in self.courses.keys():
            self.courses[object_id] = CourseConfig(
                update_task=None,
                availability_tasks=[]
            )

        task.merge_into_course(self.courses[object_id])

class IliasConfig(BaseModel):
    username: str
    password: str
    domain: str

