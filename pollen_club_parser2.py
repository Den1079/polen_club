import csv
import requests
import time
import datetime
import logging
import os
import argparse

_logger = logging.getLogger(__name__)
data = 1663689791
def setup_logging(logfile, loglevel='DEBUG'):
    """
    :param logfile:
    :param loglevel:
    :return:
    """

    loglevel = getattr(logging, loglevel)

    logger = logging.getLogger()
    logger.setLevel(loglevel)
    fmt = '%(asctime)s: %(levelname)s: %(filename)s: ' + \
          '%(funcName)s(): %(lineno)d: %(message)s'
    formatter = logging.Formatter(fmt)

    fh = logging.FileHandler(filename=logfile)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


def main(delay):
    """
    :param delay: delay of web requests
    :return:
    """
    token = '7b15c74f7b15c74f7b15c74f717805135b77b157b15c74f1825b71429e94b9034cf43e3'
    version = 5.131 # версия API
    domain = 'pollen.club'  # id группы
    count = 100 # кол-во постов max можно 100
    offset = 0  # смещение для увелечения постов, если надо больше 100

    # сбор постов
    all_post = []
    _logger.info("Start parsing")
    while offset < 1000:
        response_well = requests.get('https://api.vk.com/method/wall.get',
                                params = {'access_token': token,
                                          'v': version,
                                          'domain': domain,
                                          'count': count,
                                          'offset': offset
                                          }
                                )
        offset += count
        time.sleep(delay/1000)
        if response_well.status_code != 200:
            _logger.warning("Can not get a page")
            continue
        data_wel = response_well.json()['response']['items']
        all_post.extend(data_wel)


    #  поиск комментариев в постах группы
    all_comments = []
    _logger.info("Parse comments")
    for post in all_post:
        if post['from_id'] == -87598739:
            response_comments = requests.get('https://api.vk.com/method/wall.getComments',
                                             params= {'access_token': token,
                                                      'v': version,
                                                      'owner_id': -87598739, # id группы
                                                      'post_id': post['id'], # id поста
                                                      'count': 100 # кол-во постов max можно 100
                                                      }
                                             )
            if response_comments.status_code != 200:
                _logger.warning("Can not get a page")
                continue

            if "error" in response_comments.json():
                _logger.warning(response_comments.json()["error"]["error_msg"])
                continue

            data_comments = response_comments.json()['response']['items']
            all_comments.extend(data_comments)
            time.sleep(delay/1000)


    with open("polen_club.csv", "w", encoding='utf8') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(('post_id','data','user_id', 'post'))
        try:
            for item in all_comments:
                # @TODO: add more information (date, id user)
                csv_file.writerow((item['post_id'],
                                   datetime.datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S'),
                                   item['from_id'],
                                   item['text']))
        except (FileNotFoundError, IOError) as err:
            _logger.error("Could not save file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser PollenClub")
    parser.add_argument("--delay", default=500, help="Request delay", dest="delay")
    args = parser.parse_args()

    setup_logging("parser.log", "INFO")
    main(int(args.delay))

# @TODO:
# 1. Select given dates
# 2. Mark nested comments

