from flask import Flask, render_template, request
from mongokit import Connection, Document
from twilio.rest import TwilioRestClient

app = Flask(__name__)

app.config.from_object('config.Config')
twilio = TwilioRestClient(app.config['ACCOUNT_ID'], app.config['API_KEY'])

class Player(Document):
    structure = {
        'name': unicode,
        'phone': unicode,
    }
    required_fields = ['name', 'phone']
    use_dot_notation = True

connection = Connection()
connection.register([Player])
triplets = connection.games.triplets
quads = connection.games.quads 
singles = connection.games.singles
persistent = connection.games.singles

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
        elif singles.count() + count >= i:
            i -= count;
            while --i > 0:
                single = singles.find_one()
                singles.remove({'_id':single['_id']})
            ready = True
        if ready:
            collection.remove()
        return ready
    if 'updates' in request.form:
        addTo(persistent)
    if request.form['size'] == '3':
        addTo(triplets)
        ready = checkReady(triplets, 3)
    elif request.form['size'] == '4':
        addTo(quads)
        ready = checkReady(quads, 4)
    elif request.form['size'] == '0':
        addTo(singles)
        ready == checkReady(quads, 4) or checkReady(triplets, 3)
        if singles.count() == 3:
            singles.remove()
            ready = True
    if ready:
        return "play!"
    else:
        return "we'll let you know"

@app.route('/players')
def list():
    return render_template('players.html',
                            quads=quads.Player.find(),
                            triplets=triplets.Player.find(),
                            singles=singles.Player.find())
 
if __name__ == '__main__':
    app.run(debug=True)

