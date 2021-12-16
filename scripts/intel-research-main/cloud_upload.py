from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import ntpath

def uploadFile(path):
	# Below code does the authentication
	# part of the code
	gauth = GoogleAuth()
	gauth.LoadCredentialsFile("mycreds.txt")
	if gauth.credentials is None:
		# Authenticate if they're not there
		gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
		# Refresh them if expired
		gauth.Refresh()
	else:
		# Initialize the saved creds
		gauth.Authorize()
	# Save the current credentials to a file
	gauth.SaveCredentialsFile("mycreds.txt")

	drive = GoogleDrive(gauth)

	filename = ntpath.basename(path)
	print('...copying file ' + filename + ' to the cloud')
	f = drive.CreateFile({'title': filename, 'parents': [{'id': '1cfUKluTLdhZ8aVMEYhwumc-XBCY8L23S'}]})
	f.SetContentFile(path)
	f.Upload()
	f = None