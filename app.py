import os
import logging
import re
import time
import transfer_data
from os.path import join, dirname
from dotenv import load_env
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SockertModeHandler

dotenv_path = join(dirname(__file__), '.\\.env')
load_env(dotenv_path)

logging.basicConfig(level=logging.DEBUG)

DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

@app.message(re.compile('^url (.*)$', re.IGNORECASE))
def url(say, context, logger):
    #user_id = context['user_id']
    url = context['matches'][0]
    transferData = TransferData(DROPBOX_ACCESS_TOKEN)
    try:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_from = f'{timestr}.pdf'
        pdfkit.from_url(url, file_from)
        
        file_to = '/Supernote/bot/{file_from}.pdf'
        transferData.upload_file(file_from=file_from, file_to=file_to)
    

