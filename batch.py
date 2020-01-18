from datetime import datetime, timedelta
import os
from template.batch import collect_new_graduate_engineers, collect_new_graduate_designers

MODE = os.environ['MODE']


def execute():
    jp_time = datetime.now()
    # 本番環境はHerokuのUSタイムゾーンに置く想定なので、9時間足して日本時間判定できるようにする。
    if MODE == 'PRODUCTION':
        jp_time += timedelta(hours=9)
    # Spread Sheetを手動で触っていない時間に動かしたいので、深夜に起動するようにしている。
    if jp_time.hour == 0:
        collect_new_graduate_engineers.execute()
    elif jp_time.hour == 3:
        collect_new_graduate_designers.execute()
    else:
        print(f'バッチ起動時間ではなかったので処理終了。現在時間(日本): {jp_time}')


if __name__ == "__main__":
    execute()
