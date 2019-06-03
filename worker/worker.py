import redis
import json 
from time import sleep
from random import randint

if __name__ == '__main__':
    redis = redis.Redis(host='queue', port='6379', db='0')
    while True:
        mail = json.loads(redis.blpop('sender')[1])
        print('Sending mail:', mail['subject'], '...')
        sleep(randint(10,30))
        print('mail', mail['subject'], 'sent with success!')
