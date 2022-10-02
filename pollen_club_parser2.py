import csv
import requests
import time

token = '7b15c74f7b15c74f7b15c74f717805135b77b157b15c74f1825b71429e94b9034cf43e3'
version = 5.131 # версия API
domain = 'pollen.club'  # id группы
count = 100 # кол-во постов max можно 100
offset = 1000  # смещение для увелечения постов, если надо больше 100
# сбор постов
all_post = []
while offset < 1000:
    response_well = requests.get('https://api.vk.com/method/wall.get',
                            params = {'access_token':token,
                                      'v':version,
                                      'domain':domain,
                                      'count': count,
                                      'offset':offset
                                      }
                            )
    data_wel = response_well.json()['response']['items']
    offset += 100
    all_post.extend(data_wel)
    time.sleep(0.5)
#  поиск комментариев в постах группы
all_comments = []
for i in range(len(all_post)):
    if all_post[i]['from_id'] == -87598739:
        response_comments = requests.get('https://api.vk.com/method/wall.getComments',
                                         params= {'access_token': token,
                                                  'v': version,
                                                  'owner_id': -87598739, # id группы
                                                  'post_id': all_post[i]['id'], # id поста
                                                  'count': 100 # кол-во постов max можно 100
                                                  }
                                         )
        data_comments = response_comments.json()['response']['items']
        all_comments.extend(data_comments)
        time.sleep(0.5)


with open("polen_club.csv", "w", encoding='utf8') as file:
    csv_file = csv.writer(file)
    csv_file.writerow(('post_id','data','post'))
    for item in all_comments:
        csv_file.writerow((item['post_id'],item['date'],item['text']))


