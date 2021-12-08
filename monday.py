# pip install flask for this to work
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
    return 'hello <b>world</b>'

@app.route('/users')
def users():
    return render_template('users.html', username='Mike')


app.run()
