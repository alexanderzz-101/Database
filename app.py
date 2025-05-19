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
    cursor = db.cursor(dictionary=True)
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

        return redirect(url_for('vendors'))

    return render_template('add_vendor.html')

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        name = request.form['name']
        category = request.form['category']
        unit = request.form['unit']
        cursor.execute("""
            INSERT INTO Products (vendor_id, name, category, unit) 
            VALUES (%s, %s, %s, %s)
        """, (vendor_id, name, category, unit))
        db.commit()
        return redirect(url_for('products'))

    cursor.execute("SELECT * FROM Vendors")
    vendors = cursor.fetchall()
    return render_template('add_product.html', vendors=vendors)


@app.route('/vendors/edit/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        stall_number = request.form['stall_number']
        cursor.execute("""
            UPDATE vendors
            SET name = %s, contact_info = %s, stall_number = %s
            WHERE vendor_id = %s
        """, (name, contact_info, stall_number, vendor_id))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('vendors'))

    cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
    vendor = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template('edit_vendor.html', vendor=vendor)


# Route: Delete Vendor
@app.route('/vendors/delete/<int:vendor_id>', methods=['POST'])
def delete_vendor(vendor_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM vendors WHERE vendor_id = %s", (vendor_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vendors'))

@app.route('/products')
def products():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, v.name AS vendor_name 
        FROM Products p 
        JOIN Vendors v ON p.vendor_id = v.vendor_id
    """)
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('products.html', products=products)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        name = request.form['name']
        category = request.form['category']
        unit = request.form['unit']
        cursor.execute("""
            UPDATE Products 
            SET vendor_id = %s, name = %s, category = %s, unit = %s 
            WHERE product_id = %s
        """, (vendor_id, name, category, unit, id))
        db.commit()
        return redirect(url_for('products'))

    cursor.execute("SELECT * FROM Products WHERE product_id = %s", (id,))
    product = cursor.fetchone()
    cursor.execute("SELECT * FROM Vendors")
    vendors = cursor.fetchall()
    return render_template('edit_product.html', product=product, vendors=vendors)

@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Products WHERE product_id = %s", (id,))
    db.commit()
    return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True)
