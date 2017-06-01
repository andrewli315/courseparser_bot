import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file
from fsm import TocMachine


API_TOKEN = '260749343:AAF18QJQQbbA3Xd9MFtkSo2FsCCwyCEPU0w'
WEBHOOK_URL ='https://484ad4c7.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'parse',
        'dummy',
        'grade1',
        'grade2',
        'grade3',
        'grade4',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'grade1',
            'conditions': 'is_going_to_grade1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'grade2',
            'conditions': 'is_going_to_grade2'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'grade3',
            'conditions': 'is_going_to_grade3'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'grade4',
            'conditions': 'is_going_to_grade4'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'dummy',
            'conditions': 'is_going_to_dummy'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'parse',
            'conditions': 'parseweb'
        },
        {
            'trigger': 'go_back',
            'source': [
                'grade1',
                'grade2',
                'grade3',
                'grade4',
                'parse',
                'dummy'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=True,
    show_conditions=True,
)

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()




    #update = telegram.Update.de_json(request.get_json(force=True), bot)
    #chat_id = update.message.chat.id
    #print(chat_id)
    #bot.send_message(chat_id=chat_id,text="hello")
