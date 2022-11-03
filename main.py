import bot_tg
import pars_and_sql
from threading import Thread


if __name__ == "__main__":
    Thread(target=bot_tg.start_bot).start()
    Thread(target=pars_and_sql.timer).start()
