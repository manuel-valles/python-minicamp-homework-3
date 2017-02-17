from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods={'POST'})
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free = request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods(name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES(?,?,?,?,?)', (name,calories,cuisine,is_vegetarian,is_gluten_free))
        connection.commit()
        message = 'Record successfully added'
    except:
        connection.rollback()
        message = 'Error in insert operation'
    finally:
        return render_template('result.html', message = message)
        connection.close()
# EXTRA CREDIT
@app.route('/favorite')
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM foods WHERE name = "Banana"')
        myfood = cursor.fetchone()
    except:
        connection.rollback()
        myfood = "Error in select operation"
    finally:
        return jsonify(myfood)
        connection.close()

@app.route('/search', methods={'GET'})
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = request.args['name']
        cursor.execute('SELECT * FROM foods WHERE name = ?',(name,))
        foodin = cursor.fetchone()
    except:
        foodin = "Error in select operation"
    finally:
        return jsonify(foodin)
        connection.close()

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE IF EXISTS foods')
        message="dropped"
    except:
        message = "table not dropped"
    finally:
        return message
        connection.close()
