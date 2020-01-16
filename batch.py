from datetime import datetime
from template.batch import collect_new_graduate_engineers, collect_new_graduate_designers


def execute():
    now = datetime.now()
    print('now.hour: {}'.format(now.hour))
    # TODO: 実装要修正。HerokuにデプロイするとUS時間になるので日本時間+9時間の時間指定している。
    if now.hour == 15:
        collect_new_graduate_engineers.execute()
    elif now.hour == 16:
        collect_new_graduate_designers.execute()


if __name__ == "__main__":
    execute()
