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
singles = connection.games.singles

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def signup():
    ready = False
    def addTo(collection):
        player = collection.Player()
        player['name'] = request.form['name']
        player['phone'] = request.form['phone']
        player.save()
    def checkReady(collection, i):
        count = collection.count()
        ready = False
        if count == i:
            ready = True
        elif count == i-1 and singles.count() > 0:
            single = singles.find_one()
            singles.remove({'_id':single['_id']})
            ready = True
        if ready:
            collection.remove()
        return ready
    if request.form['size'] == '3':
        addTo(triplets)
        ready = checkReady(triplets, 3)
    elif request.form['size'] == '4':
        addTo(quads)
        ready = checkReady(quads, 4)
    elif request.form['size'] == '0':
        addTo(singles)
        ready == checkReady(quads, 4) or checkReady(triplets, 3)
    if ready or singles.count() == 3:
        return "play!"
    else:
        return "we'll let you know"
    #return request.form['name'] + ':' + request.form['phone'] + '-' + request.form['size'] + '-' + request.form['updates']

@app.route('/players')
def list():
    string = str(quads.count()) + ' Quad Players:<br>'
    for player in quads.Player.find():
         string += player.name + ':' + player.phone + '<br>'
    string += str(triplets.count()) + ' Triplet Players:<br>'
    for player in triplets.Player.find():
         string += player.name + ':' + player.phone + '<br>'
    string += str(singles.count()) + ' Single Players:<br>'
    for player in singles.Player.find():
         string += player.name + ':' + player.phone + '<br>'
    return string
 
if __name__ == '__main__':
    app.run(debug=True)

