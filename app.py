from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

app = Flask(__name__)


english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)

# Define the expected username and password
expected_username = 'admin'
expected_password = 'admin'

@app.route('/login')
def login_page():
    return render_template('Loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == expected_username and password == expected_password:
        # Successful login, redirect to index page
        return redirect(url_for('index_page'))
    else:
        # Invalid username or password, show an error message
        return render_template('Loginpage.html', error_message='Enter a Valid Username and Password')

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/index")
def index_page():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
