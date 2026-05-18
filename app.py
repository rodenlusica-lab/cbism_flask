from flask import Flask,render_template,request,redirect,session
from config import cursor
from models.product import Product
import random

# =========================================
# FLASK APPLICATION
# =========================================
app=Flask(__name__)

# =========================================
# ENCAPSULATION
# =========================================
app.secret_key="cbism_secret_key"

# =========================================
# USER CLASS
# =========================================
class User:

    # Constructor
    def __init__(self,email,password):
        self.email=email
        self.password=password

    # Method
    def authenticate(self):

        sql="SELECT * FROM users WHERE email=%s AND password=%s"

        cursor.execute(sql,(self.email,self.password))

        return cursor.fetchone()

# =========================================
# INHERITANCE
# =========================================
class Admin(User):

    # Polymorphism
    def authenticate(self):

        sql="SELECT * FROM users WHERE email=%s AND password=%s"

        cursor.execute(sql,(self.email,self.password))

        return cursor.fetchone()

# =========================================
# LOGIN ROUTE
# =========================================
@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        # Object Creation
        admin=Admin(email,password)

        # Method Call
        user=admin.authenticate()

        if user:

            session["user_id"]=user["id"]

            return redirect("/dashboard")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# =========================================
# DASHBOARD
# =========================================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    product=Product()

    products=product.get_all_products()

    return render_template(
        "dashboard.html",
        products=products
    )

# =========================================
# ADD PRODUCT
# =========================================
@app.route("/add_product",methods=["GET","POST"])
def add_product():

    if "user_id" not in session:
        return redirect("/")

    if request.method=="POST":

        name=request.form["name"]
        category=request.form["category"]
        stock=request.form["stock"]
        price=request.form["price"]

        product_id=f"P-{random.randint(1000,9999)}"

        product=Product(
            product_id,
            name,
            category,
            stock,
            price
        )

        product.add_product()

        return redirect("/dashboard")

    return render_template("add_product.html")

# =========================================
# DELETE PRODUCT
# =========================================
@app.route("/delete_product/<product_id>")
def delete_product(product_id):

    if "user_id" not in session:
        return redirect("/")

    product=Product(product_id=product_id)

    product.delete_product()

    return redirect("/dashboard")


# =========================================
# EDIT PRODUCT
# =========================================
@app.route("/edit_product/<product_id>",methods=["GET","POST"])
def edit_product(product_id):

    if "user_id" not in session:
        return redirect("/")

    product=Product(product_id=product_id)

    if request.method=="POST":

        product.name=request.form["name"]
        product.category=request.form["category"]
        product.stock=request.form["stock"]
        product.price=request.form["price"]

        product.update_product()

        return redirect("/dashboard")

    single_product=product.get_product_by_id()

    return render_template(
        "edit_product.html",
        product=single_product
    )

# =========================================
# PROCESS SALES
# =========================================
@app.route("/process_sales",methods=["GET","POST"])
def process_sales():

    if "user_id" not in session:
        return redirect("/")

    product=Product()

    products=product.get_all_products()

    receipt=None

    if request.method=="POST":

        product_id=request.form["product_id"]

        qty=int(request.form["qty"])

        product=Product(product_id=product_id)

        success=product.process_sale(qty)

        if success:

            updated_product=product.get_product_by_id()

            receipt={
                "product": updated_product["Product_Name"],
                "price": updated_product["Unit_Price"],
                "qty": qty,
                "total": qty * updated_product["Unit_Price"],
                "remaining_stock": updated_product["Stock_Quantity"]
            }

        else:
            return "Not enough stock"

    return render_template(
        "process_sales.html",
        products=products,
        receipt=receipt
    )

# =========================================
# REPORTS
# =========================================
@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/")

    product=Product()

    # SALES REPORT
    reports=product.get_sales_reports()

    # TOTAL SALES
    total_sales=product.get_total_sales()

    # ACTIVITY LOGS
    logs=product.get_activity_logs()

    # LOW STOCK
    low_products=product.get_low_stock_products()

    return render_template(
        "reports.html",
        reports=reports,
        total_sales=total_sales,
        logs=logs,
        low_products=low_products
    )

# =========================================
# LOGOUT
# =========================================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# =========================================
# RUN APPLICATION
# =========================================
if __name__=="__main__":
    app.run(debug=True)