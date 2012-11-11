from flask import Flask, render_template, request

app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def signup():
    return request.form['name'] + ':' + request.form['phone']
 
if __name__ == '__main__':
    app.run(debug=True)

