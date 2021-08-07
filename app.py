import os
import logging
import dropbox
import re
import pdfkit
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

dotenv_path = join(dirname(__file__), '.\\.env')
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)

path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

@app.command('/help')
def help(ack, say, command):
    ack()
    say(f"Hello <@{command['user']}>")

@app.command('/url')
def url(ack, say, command):
    ack()
    url = command['text']
    logging.info('\n\n'+url+'\n\n')
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    filename = 'bot_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.pdf'
    file_from = filename
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'javascript-delay':200}
    if pdfkit.from_url(url, file_from, configuration=config, options=options):
        file_to = f'/bot/{filename}'
        with open(file_from, 'rb') as f:
            if dbx.files_upload(f.read(), file_to, mode=WriteMode('overwrite')):
                #if dbx.files_move(file_to, '/../../Supernote/bot'):
                say('File uploaded sucessfully')
            else:
                say('Upload failed')
    
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()