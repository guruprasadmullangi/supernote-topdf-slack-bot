import os
import logging
import dropbox
import re
import sys
import pdfkit
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)

path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

@app.command('/help')
def help(ack, command):
    ack(f"Hello <@{command['user_id']}>\n\n"\
         "Use `/url <URL>` command to convert a webpage to pdf and upload to Dropbox to easily read on your Supernote devices.\n\n"\
         "Use `/delete` command to delete all files from `Dropbox/Supernote/Export/bot` folder in Dropbox")

@app.command('/url')
def url(ack, say, command, logger):
    url = command['text']
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    filename = 'bot_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.pdf'
    file_from = filename
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'javascript-delay':1000}
    ack('working on it...')
    try:
        if pdfkit.from_url(url, file_from, configuration=config, options=options):
            file_to = f'ns:9871776400/Supernote/EXPORT/bot/{filename}'
            with open(file_from, 'rb') as f:
                if dbx.files_upload(f.read(), file_to, mode=WriteMode('overwrite')):
                    say('Pdf ready to read on your device.')
                else:
                    say('Job failed.')
    except:
        logger.info(sys.exc_info())
        say(f"Oops!{sys.exc_info()[0]}occurred.")

@app.command('/delete')
def url(ack, say, logger):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    ack('Deleting files...')
    try:
        response = dbx.files_list_folder('ns:9871776400/Supernote/EXPORT/bot/')
        #logger.info('\n\n')
        #logger.info(response)
        for entry in response.entries:
            #logger.info(entry.name)
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.startswith('bot_') and entry.name.endswith('.pdf'):
                dbx.files_delete_v2(f'ns:9871776400/Supernote/EXPORT/bot/{entry.name}')
        if not dbx.files_list_folder('ns:9871776400/Supernote/EXPORT/bot/').entries:
            say(f'Deleted all bot files.')
        else:
            say(f'Trouble deleting files.')
    except:
        logger.info(sys.exc_info())
        say(f"Oops!{sys.exc_info()[0]}occurred.")

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()