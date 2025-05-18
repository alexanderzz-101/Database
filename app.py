from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Vendors")
    vendors = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('home.html', vendors=vendors)

@app.route('/add-vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        stall_number = request.form['stall_number']

        db = get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Vendors (name, contact_info, stall_number) VALUES (%s, %s, %s)", 
                       (name, contact_info, stall_number))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('home'))

    return render_template('add_vendor.html')

if __name__ == '__main__':
    app.run(debug=True)



