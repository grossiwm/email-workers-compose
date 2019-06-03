import psycopg2
from bottle import Bottle, request
import redis
import json

class Sender(Bottle): 
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        self.queue = redis.StrictRedis(host='queue', port='6379', db=0)
        DSN = 'dbname=email_sender user=postgres host=db'
        self.connection = psycopg2.connect(DSN)

    def register_message(self, subject, message):
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'
        cursor = self.connection.cursor()
        cursor.execute(SQL, (subject, message))
        self.connection.commit()
        cursor.close()

        mail = {'subject': subject, 'message': message}
        self.queue.rpush('sender', json.dumps(mail))

        print('Message registered!')

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')
        self.register_message(subject, message)
        return 'Message already in the queue! Subject: {} Message: {}'.format(subject, message)

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)