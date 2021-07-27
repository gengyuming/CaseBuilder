from enum import Enum


class Priority(Enum):
    PRIORITY_1 = 'High'
    PRIORITY_2 = 'Normal'
    PRIORITY_3 = 'Low'
    PRIORITY_4 = ''


class CaseStatus(Enum):
    DRAFT = 'Draft'
    DEPRECATED = 'Deprecated'
    APPROVED = 'Approved'


class ResultStatus(Enum):
    NOT_EXECUTED = 'Not Executed'
    IN_PROGRESS = 'In Progress'
    PASS = 'Pass'
    FAIL = 'Fail'
    BLOCKED = 'Blocked'




