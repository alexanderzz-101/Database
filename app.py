from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

# Homepage with navigation options
@app.route('/')
def index():
    return render_template('home.html')

# Display all vendors
@app.route('/vendors')
def vendors():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Vendors")
    vendors = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('vendors.html', vendors=vendors)

# Add a new vendor
@app.route('/add-vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        stall_number = request.form['stall_number']

        db = get_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Vendors (name, contact_info, stall_number) VALUES (%s, %s, %s)",
            (name, contact_info, stall_number)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('vendors'))  # Go back to vendors list

    return render_template('add_vendor.html')

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    db = get_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        name = request.form['name']
        category = request.form['category']
        unit = request.form['unit']

        cursor.execute(
            "INSERT INTO Products (vendor_id, name, category, unit) VALUES (%s, %s, %s, %s)",
            (vendor_id, name, category, unit)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('vendors'))

    # On GET request, fetch vendors to select from
    cursor.execute("SELECT vendor_id, name FROM Vendors")
    vendors = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('add_product.html', vendors=vendors)




if __name__ == '__main__':
    app.run(debug=True)
