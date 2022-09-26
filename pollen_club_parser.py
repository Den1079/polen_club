import csv
import requests
import time


token = '7b15c74f7b15c74f7b15c74f717805135b77b157b15c74f1825b71429e94b9034cf43e3'
version = 5.131
domain = 'pollen.club'
count = 100
offset = 0
all_post = []
while offset < 1000:
    response = requests.get('https://api.vk.com/method/wall.get',
                            params = {'access_token':token,
                                      'v':version,
                                      'domain':domain,
                                      'count': count,
                                      'offset':offset
                                      }
                            )
    data = response.json()['response']['items']
    offset += 100
    all_post.extend(data)
    time.sleep(0.5)

with open("polen_club.csv", "w", encoding='utf8') as file:
    csv_file = csv.writer(file)
    csv_file.writerow(('id','data','post'))
    for item in all_post:
        csv_file.writerow((item['id'],item['date'],item['text']))
