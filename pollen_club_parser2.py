import csv
import requests
import time

token = '7b15c74f7b15c74f7b15c74f717805135b77b157b15c74f1825b71429e94b9034cf43e3'
version = 5.131
domain = 'pollen.club'
count = 100 # кол-во постов мак можно 100
offset = 0  # смещение для увелечения постов
all_post = []
while offset < 1000:
    response_well = requests.get('https://api.vk.com/method/wall.get', # сбор постов
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

all_comments = []
for i in range(len(all_post)):
    if all_post[i]['from_id'] == -87598739: #  поиск постов группы
        response_comments = requests.get('https://api.vk.com/method/wall.getComments', #  сбор коментариев постов группы
                                         params= {'access_token': token,
                                                  'v': version,
                                                  'owner_id': -87598739, # id группы
                                                  'post_id': all_post[i]['id'], # id поста
                                                  'count': 100 # кол-во постов мак можно 100
                                                  }
                                         )
        data_comments = response_comments.json()
        all_comments.extend(data_comments)


with open("polen_club.csv", "w", encoding='utf8') as file:
    csv_file = csv.writer(file)
    csv_file.writerow(('id','data','post'))
    for item in all_comments:
        csv_file.writerow((item['id'],item['date'],item['text']))
print()


