import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token
 
    def upload_file(self, file_from=None, file_to=None):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)
        #files_upload(f, path, mode=WriteMode('add', None), autorename=False, client_modified=None, mute=False)
 
        with open(file_from, 'rb') as f:
            dbx.files_upload(f, file_to)