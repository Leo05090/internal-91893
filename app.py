from flask import Flask, render_template
import sqlite3
from flask import g

DATABASE = 'daitabaice.db'

# intialise the flask app
app = Flask(__name__) 

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
 
@app.route('/')
def home():
    sql = """
        SELECT admirals.admiralsID, admirals.admirals_name, countries.name, admirals.image, admirals.birth, admirals.deceased, admirals.class, admirals.admirals_detail, admirals.class, admirals.eventID
        FROM admirals
        INNER JOIN countries
        ON admirals.countryID = countries.countryID;
    """
    results = query_db(sql)
    return render_template('home.html', results=results)

@app.route('/admirals/<int:id>')
def admiral(id):
    sql = """
        SELECT admirals.admiralsID, admirals.admirals_name, countries.name , admirals.birth, admirals.deceased, admirals.class, admirals.admirals_detail, admirals.countryID, admirals.image, admirals.eventID, countries.image
        FROM admirals
        JOIN countries ON countries.countryID = admirals.countryID
        WHERE countries.countryID = ?
    """
    result = query_db(sql, (id,), one=True)
    return render_template('admirals.html', admiral=result)

@app.route('/events')
def event():
    sql = """
        SELECT event.event_name, event.event_year, event.event_detail
        FROM event;
    """
    results = query_db(sql)
    return render_template('event.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)