import psycopg2
from bottle import route, run, request

DSN = 'dbname=email_sender user=postgres host=db'
SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'

def register_message(subject, message):
    connection = psycopg2.connect(DSN)
    cursor = connection.cursor()
    cursor.execute(SQL, (subject, message))
    connection.commit()
    cursor.close()
    connection.close()

    print('Message registered!')

@route('/', method='POST')
def send():
    subject = request.forms.get('subject')
    message = request.forms.get('message')
    register_message(subject, message)
    return 'Message already in the queue! Subject: {} Message: {}'.format(subject, message)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)