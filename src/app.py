from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdictionary.db'
db = SQLAlchemy(app)


class DictionaryTerm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(256), nullable=False)
    definition = db.Column(db.String(4096), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Term %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    search_result = request.args.get('term')
    allTerms = DictionaryTerm.query.filter(DictionaryTerm.term.like("%"+search_result+"%")).all()


    return render_template('search_result.html', terms=allTerms)


@app.route('/additem', methods=["GET", "POST"])
def addItem():
    if request.method == 'POST':
        term_content = request.form['term']
        term_definition = request.form['definition']

        new_term = DictionaryTerm(term=term_content, definition=term_definition)

        try:
            db.session.add(new_term)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the term'
    else:
        return render_template('add_item.html')

    return render_template('add_item.html')


if __name__ == "__main__":
    app.run(debug=True)

