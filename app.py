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
        SELECT ships.shipID, ships.name, countries.name, ships.image
        FROM ships
        INNER JOIN countries
        ON ships.countryID = countries.countryID;
    """
    results = query_db(sql)
    return render_template('home.html', results=results)

@app.route('/ships/<int:id>')
def ship(id):
    sql = """
        SELECT ships.shipID, ships.name, countries.name , ships.Standard_Displacement, ships.Full_Load_Displacement, ships.size_of_cannon, ships.image
        FROM ships
        JOIN countries ON countries.countryID = ships.countryID
        WHERE countries.countryID = ?
    """
    result = query_db(sql, (id,), one=True)
    return render_template('ship.html', ship=result)

if __name__ == "__main__":
    app.run(debug=True)