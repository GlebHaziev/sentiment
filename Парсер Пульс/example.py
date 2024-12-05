import datetime
import traceback
import pandas as pd
import win32com.client as win32
import traceback
from database import conn
from time import sleep
from tpulse import TinkoffPulse
from random import choice
from httpx import (
    HTTPStatusError, ConnectError, ConnectTimeout, ReadTimeout
)

from utils import convert_dt, logger, get_dt
from database import insert, cursor, conn


def parse_post_by_ticker(post: dict) -> dict:
    post_data = {
        "post_id": post["id"],
        "inserted": convert_dt(post["inserted"]),
        "instruments": ", ".join([i["ticker"] for i in post["content"]["instruments"]])
        if len(post["content"]["instruments"]) > 0
        else None,
        "hashtags": ", ".join([i["title"] for i in post["content"]["hashtags"]])
        if len(post["content"]["hashtags"]) > 0
        else None,
        "content": post["content"]["text"],
        "parse_dt": get_dt(),
    }
    insert("tcs_pulse_posts", post_data)
    return post_data


def get_tickers_list() -> list:
    with open("tickers.txt", "r") as f:
        _tickers = f.read()
        tickers = [i.strip() for i in _tickers.split("\n")]
    return tickers


def parse_posts_by_ticker_list():
    ERRORS = []

    pulse = TinkoffPulse()
    tickers = get_tickers_list()  # Получаем список тикеров
    for ticker in tickers:
        fetch_cursor = 999999999

        for step in range(1, 5):  # Примерно ожидаемое кол-во постов, где 1 итерация = 30 постов, т.е. полный набор будет <= 250 * 30 постов по одному тикеру
            logger.info(f"Прокрутка для тикера {ticker} № {step}")
            try:
                posts_from_ticker = pulse.get_posts_by_ticker(ticker=ticker, cursor=fetch_cursor)
                fetch_cursor = posts_from_ticker["nextCursor"]
                posts = posts_from_ticker["items"]
                logger.info(f"Кол-во постов в текущей итерации = {len(posts)}")
                if len(posts) == 0:
                    logger.info(f"Для тикера {ticker} больше нет постов, переключаем на следующий элемент цикла")
                    break
                for post in posts:
                    parse_post_by_ticker(post)
                sleep(choice(range(1, 3)))
            except (HTTPStatusError, ConnectError, ConnectTimeout, ReadTimeout):
                logger.error(f"Ошибка! Пауза 25 секунд {traceback.format_exc()}")
                sleep(25)
                ERRORS.append([ticker, fetch_cursor])
            except Exception:
                logger.error(f"Not excepted error {traceback.format_exc()}")
                sleep(15)
                ERRORS.append([ticker, fetch_cursor])
            finally:
                pulse = TinkoffPulse()
        
    for item in ERRORS:
        try:
            posts_from_ticker = pulse.get_posts_by_ticker(ticker=item[0], cursor=item[1])
            posts = posts_from_ticker["items"]
            logger.info(f"Кол-во постов в текущей итерации = {len(posts)}")
            if len(posts) == 0:
                break
            for post in posts:
                parse_post_by_ticker(post)
            sleep(choice(range(1, 3)))
        except Exception:
            logger.error(f"Not excepted error {traceback.format_exc()}")
            sleep(25)

    logger.info(f"ticker {ticker} is done!")


def export_to_excel():
    try:
        sql3_query = "SELECT * FROM tcs_pulse_posts;"
        resultDF = pd.read_sql_query(sql3_query, conn)

        # Укажите имя файла Excel
        excel_file = 'all_posts.xlsx'

        # Сохраняем DataFrame в Excel файл
        resultDF.to_excel(excel_file, index=False)

        # Открываем Excel и сохраняем файл
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(excel_file)
        excel.Visible = False  # Установите False, если не хотите показывать Excel
        wb.Close(SaveChanges=True)  # Закрываем файл, сохраняя изменения
        excel.Quit()  # Закрываем приложение Excel
        print("Данные успешно экспортированы в", excel_file)

    except Exception as e:
        print("Произошла ошибка при экспорте в Excel:", e)
        print(traceback.format_exc())

# Вызов функции
parse_posts_by_ticker_list()
export_to_excel()