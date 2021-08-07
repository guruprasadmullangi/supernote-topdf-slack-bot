import os
import logging
import re
from datetime import datetime
import pdfkit
from os.path import join, dirname
from dotenv import load_dotenv
from slack_bolt import App
from transfer_data import TransferData
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv_path = join(dirname(__file__), '.\\.env')
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)

path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

@app.message(re.compile('^help$', re.IGNORECASE))
def help(message, say):
    say(f"Hello <@{message['user']}>")

@app.message(re.compile('^url (.*)$', re.IGNORECASE))
def url(say, context, logger):
    url = context['matches'][0]
    url_correct = url[1:-1]
    transferData = TransferData(DROPBOX_ACCESS_TOKEN)
    filename = 'bot_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.pdf'
    file_from = filename
    logger.info(file_from)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'javascript-delay':5000}
    pdfkit.from_url(url_correct, file_from, configuration=config, options=options)
    
    file_to = f'/bot/{filename}'

    if transferData.upload_file(file_from=file_from, file_to=file_to):
        say('done')
    else:
        say('fail')
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()