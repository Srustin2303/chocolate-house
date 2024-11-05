from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def get_db_connection():
    conn = sqlite3.connect("chocolate_house.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    connect = get_db_connection()
    cursor = connect.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        suggestion TEXT,
        allergen_concerns TEXT,
        date_submitted DATE
    );
    ''')

    connect.commit()
    connect.close()

init_db()

def add_seasonal_flavor(name, description, start_date, end_date):
    connect = get_db_connection()
    cursor = connect.cursor()

    cursor.execute('''
    INSERT INTO seasonal_flavors (name, description, start_date, end_date)
    VALUES (?, ?, ?, ?)
    ''', (name, description, start_date, end_date))

    connect.commit()
    connect.close()

def add_ingredient(name, quantity):
    if quantity < 0:
        return

    connect = get_db_connection()
    cursor = connect.cursor()

    cursor.execute('''
    INSERT INTO ingredients (name, quantity)
    VALUES (?, ?)
    ''', (name, quantity))

    connect.commit()
    connect.close()

def add_customer_feedback(customer_name, suggestion, allergen_concerns):
    if not customer_name or not suggestion:
        return

    connect = get_db_connection()
    cursor = connect.cursor()

    cursor.execute('''
    INSERT INTO customer_feedback (customer_name, suggestion, allergen_concerns, date_submitted)
    VALUES (?, ?, ?, DATE('now'))
    ''', (customer_name, suggestion, allergen_concerns))

    connect.commit()
    connect.close()

@app.route('/')
def index():
    conn = get_db_connection()
    flavors = conn.execute("SELECT * FROM seasonal_flavors").fetchall()
    conn.close()
    return render_template('index.html', flavors=flavors)

@app.route('/add_flavor', methods=['POST'])
def add_flavor():
    flavor_name = request.form['flavor_name']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    add_seasonal_flavor(flavor_name, description, start_date, end_date)
    flash("Seasonal flavor added successfully!")
    return redirect(url_for('index'))

@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    ingredients = conn.execute("SELECT * FROM ingredients").fetchall()
    conn.close()
    return render_template('inventory.html', ingredients=ingredients)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient_route():
    ingredient_name = request.form['ingredient_name']
    quantity = int(request.form['quantity'])

    add_ingredient(ingredient_name, quantity)
    flash("Ingredient added successfully!")
    return redirect(url_for('inventory'))

@app.route('/suggestions')
def suggestions():
    conn = get_db_connection()
    suggestions = conn.execute("SELECT * FROM customer_feedback").fetchall()
    conn.close()
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/add_suggestion', methods=['POST'])
def add_suggestion():
    customer_name = request.form['customer_name']
    suggestion = request.form['flavor_suggestion']
    allergen_concerns = request.form['allergy_concern']

    add_customer_feedback(customer_name, suggestion, allergen_concerns)
    flash("Customer suggestion added successfully!")
    return redirect(url_for('suggestions'))

if __name__ == "__main__":
    app.run(debug=True)
