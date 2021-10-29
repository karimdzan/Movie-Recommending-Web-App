from flask import Flask,render_template,request,redirect
from rec import Rec
import re

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

app = Flask(__name__,template_folder='templates')
@app.route('/')
def home():
     return render_template('app.html')

@app.route('/results',methods=['POST'])
def results():
    value = request.form['movie']
    if has_cyrillic(value):
        return render_template('results.html',text='Enter the movie in english')
    movie_list = Rec(value)
    if request.method == 'POST':
        return render_template('results.html',movie_list=movie_list)

if __name__ == '__main__':
    app.run(debug=True)