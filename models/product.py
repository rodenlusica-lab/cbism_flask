from config import cursor, db

class Product:

    # CONSTRUCTOR
    def __init__(self,
                 product_id=None,
                 name=None,
                 category=None,
                 stock=None,
                 price=None):

        self.product_id=product_id
        self.name=name
        self.category=category
        self.stock=stock
        self.price=price

    # GET ALL PRODUCTS
    def get_all_products(self):

        sql="""
        SELECT * FROM products
        ORDER BY Date_Received DESC
        """

        cursor.execute(sql)

        return cursor.fetchall()

    # ADD PRODUCT
    def add_product(self):

        sql="""
        INSERT INTO products
        (Product_ID,Product_Name,Category,Stock_Quantity,Unit_Price)
        VALUES(%s,%s,%s,%s,%s)
        """

        values=(
            self.product_id,
            self.name,
            self.category,
            self.stock,
            self.price
        )

        cursor.execute(sql,values)

        db.commit()

    # DELETE PRODUCT
    def delete_product(self):

        sql="""
        SELECT Product_Name
        FROM products
        WHERE Product_ID=%s
        """

        cursor.execute(sql,(self.product_id,))

        product=cursor.fetchone()

        product_name=product["Product_Name"]

        sql="""
        DELETE FROM products
        WHERE Product_ID=%s
        """

        cursor.execute(sql,(self.product_id,))

        sql="""
        INSERT INTO activity_logs
        (action,product_name,details)
        VALUES(%s,%s,%s)
        """

        values=(
            "DELETE",
            product_name,
            f"Deleted Product ID: {self.product_id}"
        )

        cursor.execute(sql,values)

        db.commit()

    # GET SINGLE PRODUCT
    def get_product_by_id(self):

        sql="""
        SELECT * FROM products
        WHERE Product_ID=%s
        """

        cursor.execute(sql,(self.product_id,))

        return cursor.fetchone()

    # UPDATE PRODUCT
    def update_product(self):

        sql="""
        UPDATE products
        SET Product_Name=%s,
            Category=%s,
            Stock_Quantity=%s,
            Unit_Price=%s
        WHERE Product_ID=%s
        """

        values=(
            self.name,
            self.category,
            self.stock,
            self.price,
            self.product_id
        )

        cursor.execute(sql,values)

        sql="""
        INSERT INTO activity_logs
        (action,product_name,details)
        VALUES(%s,%s,%s)
        """

        values=(
            "UPDATE",
            self.name,
            f"Updated Product ID: {self.product_id}"
        )

        cursor.execute(sql,values)

        db.commit()

    # PROCESS SALE
    def process_sale(self,qty):

        # 🔥 Method
        # Handles sales transaction

        sql="""
        SELECT * FROM products
        WHERE Product_ID=%s
        """

        cursor.execute(sql,(self.product_id,))

        product=cursor.fetchone()

        # 🔥 Encapsulation
        current_stock=product["Stock_Quantity"]
        product_name=product["Product_Name"]
        unit_price=product["Unit_Price"]

        # CHECK STOCK
        if qty > current_stock:
            return False

        # COMPUTATION
        new_stock=current_stock - qty
        total=qty * unit_price

        # UPDATE STOCK
        sql="""
        UPDATE products
        SET Stock_Quantity=%s
        WHERE Product_ID=%s
        """

        cursor.execute(sql,(new_stock,self.product_id))

        # SAVE SALES RECORD
        sql="""
        INSERT INTO sales_records
        (product_name,quantity,total_price)
        VALUES(%s,%s,%s)
        """

        values=(
            product_name,
            qty,
            total
        )

        cursor.execute(sql,values)

        # SAVE ACTIVITY LOG
        sql="""
        INSERT INTO activity_logs
        (action,product_name,details)
        VALUES(%s,%s,%s)
        """

        values=(
            "SALE",
            product_name,
            f"Sold {qty} item(s)"
        )

        cursor.execute(sql,values)

        db.commit()

        return True

    # GET ACTIVITY LOGS
    def get_activity_logs(self):

        sql="""
        SELECT * FROM activity_logs
        ORDER BY created_at DESC
        """

        cursor.execute(sql)

        return cursor.fetchall()

    # GET LOW STOCK PRODUCTS
    def get_low_stock_products(self):

        sql="""
        SELECT * FROM products
        WHERE Stock_Quantity < 10
        """

        cursor.execute(sql)

        return cursor.fetchall()

    # GET SALES REPORTS
    def get_sales_reports(self):

        sql = """
        SELECT product_name,
               SUM(quantity) AS total_qty,
               SUM(total_price) AS total_revenue
        FROM sales_records
        GROUP BY product_name
        ORDER BY product_name
        """
            

        cursor.execute(sql)

        return cursor.fetchall()

    # GET TOTAL SALES
    def get_total_sales(self):

        sql="""
        SELECT SUM(total_price) AS total_sales
        FROM sales_records
        """

        cursor.execute(sql)

        return cursor.fetchone()