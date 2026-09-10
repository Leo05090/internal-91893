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
        SELECT admirals.admiralsID, admirals.name, countries.name, admirals.image
        FROM admirals
        INNER JOIN countries
        ON admirals.countryID = countries.countryID;
    """
    results = query_db(sql)
    return render_template('home.html', results=results)

@app.route('/admirals/<int:id>')
def ship(id):
    sql = """
        SELECT admirals.admiralsID, admirals.admirals_name, countries.name , admirals.birth, admirals.deceased, admirals.admirals_detail, admirals.Completed_year, admirals.countryID, admirals.image, admirals.eventID
        FROM admirals
        JOIN countries ON countries.countryID = ships.countryID
        WHERE countries.countryID = ?
    """
    result = query_db(sql, (id,), one=True)
    return render_template('ship.html', ship=result)

if __name__ == "__main__":
    app.run(debug=True)