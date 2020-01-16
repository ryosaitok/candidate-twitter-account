# coding=utf-8
from service import collect_candidate

# 対象のSpread SheetのID
GID = '13dKDZ8T2yJW5IlCO9pzP__iyT0H9h-X-QndP1YN5clE'


def execute():
    collect_candidate.execute(GID)
