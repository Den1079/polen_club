import csv
import requests
import time

token = '7b15c74f7b15c74f7b15c74f717805135b77b157b15c74f1825b71429e94b9034cf43e3'
version = 5.131
domain = 'pollen.club'
count = 50
offset = 0
all_post = []
while offset < 50:
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

all_comments = []
for i in range(len(all_post)):
    if all_post[i]['from_id'] == -87598739:
        response_comments = requests.get('https://api.vk.com/method/wall.getComments',
                                         params= {'access_token': token,
                                                  'v': version,
                                                  'owner_id': -87598739,
                                                  'post_id': all_post[i]['id'],
                                                  'count': 100
                                                  }
                                         )
        data_comments = response_comments.json()['response']['items']
        all_comments.extend(data_comments)


with open("polen_club.csv", "w", encoding='utf8') as file:
    csv_file = csv.writer(file)
    csv_file.writerow(('id','data','post'))
    for item in all_comments:
        csv_file.writerow((item['id'],item['date'],item['text']))
print()


