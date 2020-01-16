# coding=utf-8
from service import collect_candidate

# 対象のSpread SheetのID
GID = '1xzkVC6KtN64WmL8LbMAwM0a-pZYCHZnVrxZLPtnVc44'


def execute():
    collect_candidate.execute(GID)
