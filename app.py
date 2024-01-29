from flask import Flask
from quickstart import getFolders

app = Flask(__name__)
 
@app.route('/')
def home():
	return 'This is the home page'
 
 
@app.route('/folders')
def listFolders():
	folders = getFolders()
	if folders is None:
		return "No folders found."
	return "Folders:<br>" + "<br>".join(folders)
 
 
if __name__ == '__main__':
	app.run(debug=True)