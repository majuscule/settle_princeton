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
triplets = connection.games.triplets
quads = connection.games.quads 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def signup():
    def add(collection):
        player = collection.Player()
        player['name'] = request.form['name']
        player['phone'] = request.form['phone']
        player.save()
        if collection.count() == 3:
            connection.games.drop_collection('players')
            return "<h1>PLAY NOW</h1>"
    if request.form['size'] == 3:
        add(triplets)
    elif request.form['size'] == 4:
        add(quads)
    elif request.form['size'] == 0:
        return "<h1>We'll let you know</h1>"
    return request.form['name'] + ':' + request.form['phone'] + '-' + request.form['size'] + '-' + request.form['updates'] + '<br>SAVED'

@app.route('/players')
def list():
    string = str(collection.count()) + ' Players:<br><br>'
    for player in collection.Player.find():
         string += player.name + ':' + player.phone + '<br>'
    return string
 
if __name__ == '__main__':
    app.run(debug=True)

