from flask import Flask, render_template, request
from mongokit import Connection, Document

app = Flask(__name__)

class Player(Document):
    structure = {
        'name': unicode,
        'phone': unicode,
    }
    validators = {
        'name': lambda x: True,
        'phone': lambda x: True
    }
    required_fields = ['name', 'phone']
    use_dot_notation = True

connection = Connection()
connection.register([Player])
collection = connection.games.players

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def signup():
    player = collection.Player()
    player['name'] = request.form['name']
    player['phone'] = request.form['phone']
    player.save()
    return request.form['name'] + ':' + request.form['phone'] + '<br>SAVED'
 
if __name__ == '__main__':
    app.run(debug=True)

