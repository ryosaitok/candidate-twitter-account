from datetime import datetime
from template.batch import collect_new_graduate_engineers, collect_new_graduate_designers


def execute():
    now = datetime.now()
    if now.hour == 0:
        collect_new_graduate_engineers.execute()
    elif now.hour == 1:
        collect_new_graduate_designers.execute()


if __name__ == "__main__":
    execute()
