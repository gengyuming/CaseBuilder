from enum import EnumMeta


class Priority(EnumMeta):
    PRIORITY_1 = 'High'
    PRIORITY_2 = 'Normal'
    PRIORITY_3 = 'Low'
    PRIORITY_4 = ''


class CaseStatus(EnumMeta):
    DRAFT = 'Draft'
    DEPRECATED = 'Deprecated'
    APPROVED = 'Approved'


class ResultStatus(EnumMeta):
    NOT_EXECUTED = 'Not Executed'
    IN_PROGRESS = 'In Progress'
    PASS = 'Pass'
    FAIL = 'Fail'
    BLOCKED = 'Blocked'




