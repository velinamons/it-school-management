from enum import Enum
from typing import List, Tuple


class AgeGroup(Enum):
    JUNIOR = "6-8", "6-8 y.o."
    PRETEEN = "9-12", "9-12 y.o."
    TEENAGER = "13-15", "13-15 y.o."
    OLDER_TEEN = "16-18", "16-18 y.o."

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(item.value[0], item.value[1]) for item in cls]


class ContactMessageStatus(Enum):
    PND = "Pending"
    INP = "In Process"
    CMP = "Completed"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(item.name, item.value) for item in cls]


class ManagerRole(Enum):
    EDU_MANAGER = "Education", "Education Manager"
    PROG_MANAGER = "Program", "Program Manager"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(item.value[0], item.value[1]) for item in cls]


class GroupStatus(Enum):
    ENROLLMENT_STARTED = "enrollment_started", "Enrollment Started"
    EDUCATION_STARTED = "education_started", "Education Started"
    EDUCATION_COMPLETED = "education_completed", "Education Completed"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(item.value[0], item.value[1]) for item in cls]
