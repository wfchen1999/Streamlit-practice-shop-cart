import pandas as pd
import streamlit as st
import mysql.connector
from mysql.connector import Error
st.set_page_config(layout="wide")

# 創建一個函數 (function)，用於連接 MySQL 資料庫：
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port='3306',
            user="root",
            password="W1i3l4l6i7am",
            database="ShopCart"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(e)
    return connection

# 創建一個函數 (function)，用於新增產品：
def add_product(name, description, price, stock):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)"
            values = (name, description, price, stock)
            cursor.execute(sql, values)
            connection.commit()
            st.success("Product added successfully!")
        except Error as e:
            print(e)
            st.error("Failed to add product.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於編輯產品資訊：
def edit_product(id, name, description, price, stock):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "UPDATE products SET name=%s, description=%s, price=%s, stock=%s WHERE id=%s"
            values = (name, description, price, stock, id)
            cursor.execute(sql, values)
            connection.commit()
            st.success("Product updated successfully!")
        except Error as e:
            print(e)
            st.error("Failed to update product.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於查詢產品資訊：
def get_products():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            result = cursor.fetchall()
            # 將資料轉換為 DataFrame
            df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
            # 以表格形式呈現
            st.dataframe(df)
            # for row in result:
            #     st.write(row)
        except Error as e:
            print(e)
            st.error("Failed to get products.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於刪除產品：
def delete_product(id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM products WHERE id=%s"
            values = (id,)
            cursor.execute(sql, values)
            connection.commit()
            st.success("Product deleted successfully!")
        except Error as e:
            print(e)
            st.error("Failed to delete product.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於新增訂單：
def add_order(customer_name, customer_email, product_id, quantity):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            # Get product price
            sql = "SELECT price FROM products WHERE id=%s"
            values = (product_id,)
            cursor.execute(sql, values)
            price = cursor.fetchone()[0]
            # Add order資訊
            sql = "INSERT INTO orders (customer_name, customer_email) VALUES (%s, %s)"
            values = (customer_name, customer_email)
            cursor.execute(sql, values)
            order_id = cursor.lastrowid
            # Add order details
            sql = "INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
            values = (order_id, product_id, quantity, price)
            cursor.execute(sql, values)
            connection.commit()
            st.success("Order added successfully!")
        except Error as e:
            print(e)
            st.error("Failed to add order.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於查詢訂單：
def get_orders():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "SELECT orders.id, customer_name, customer_email, order_date, product_id, quantity, price FROM orders JOIN order_details ON orders.id = order_details.order_id"
            cursor.execute(sql)
            result = cursor.fetchall()
            # 將資料轉換為 DataFrame
            df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
            # 以表格形式呈現
            st.dataframe(df)
            # for row in result:
            #     st.write(row)
        except Error as e:
            print(e)
            st.error("Failed to get orders.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")

# 創建一個函數 (function)，用於產生報告：
def generate_report():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            # Total sales
            sql = "SELECT SUM(quantity * price) FROM order_details"
            cursor.execute(sql)
            total_sales = cursor.fetchone()[0]
            st.write("Total Sales: $", total_sales)
            # Total orders
            sql = "SELECT COUNT(DISTINCT(order_id)) FROM order_details"
            cursor.execute(sql)
            total_orders = cursor.fetchone()[0]
            st.write("Total Orders: ", total_orders)
            # Sales by product
            sql = "SELECT products.name, SUM(order_details.quantity), SUM(order_details.quantity * products.price) FROM products JOIN order_details ON products.id = order_details.product_id GROUP BY products.id"
            cursor.execute(sql)
            result = cursor.fetchall()
            # 將資料轉換為 DataFrame
            df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
            # 以表格形式呈現
            st.dataframe(df)
            # for row in result:
            #     st.write(row)
        except Error as e:
            print(e)
            st.error("Failed to generate report.")
        finally:
            cursor.close()
            connection.close()
    else:
        st.error("Database connection error.")


def customer_page():
    st.write('這是客戶端頁面。')
    # Add order form
    st.header("新增訂單")
    customer_name = st.text_input("姓名", key='CusName_Add')
    customer_email = st.text_input("Email", key='CusEmail_Add')
    product_id = st.number_input("商品 ID", key='Customer_PdID_Add', min_value=1, step=1)    #####
    quantity = st.number_input("數量", key='Quantity_Add', min_value=1, step=1)
    if st.button("新增訂單"):
        add_order(customer_name, customer_email, product_id, quantity)

    

def company_page():
    st.write('這是企業方頁面。')
    # 最後，在主程式中使用 Streamlit 的元件 (widgets) 和函數 (functions) 創建網頁介面，讓使用者可以互動地使用這些功能。
    
    # Get products button
    st.header("商品資訊")
    if st.button("查看所有商品資訊"):
        get_products()

    # Get orders button
    st.header("訂單資訊")
    if st.button("取得訂單資訊"):
        get_orders()

    # Generate report
    st.header("銷售報告")
    if st.button("取得銷售報告"):
        generate_report()

    # Add product form
    st.header("新增商品")
    name = st.text_input("輸入商品名稱", key='PdName_Add')
    description = st.text_input("簡單描述商品", key='Description_Add')
    price = st.number_input("價格", key='Price_Add', min_value=0.0, step=0.01)
    stock = st.number_input("庫存", key='Stock_Add', min_value=0, step=1)
    if st.button("新增產品"):
        add_product(name, description, price, stock)

    # Edit product form
    st.header("編輯商品")
    id = st.number_input("輸入要修改的商品 ID", key='PdID_Edit', min_value=1, step=1)
    name = st.text_input("修改商品名稱", key='PdName_Edit')
    description = st.text_input("修改商品描述", key='Description_Edit')
    price = st.number_input("修改價格", key='Price_Edit', min_value=0.0, step=0.01)
    stock = st.number_input("修改庫存", key='Stock_Edit', min_value=0, step=1)
    if st.button("確認修改"):
        edit_product(id, name, description, price, stock)

    # Delete product form
    st.header("刪除商品")
    id = st.number_input("輸入要刪除的商品 ID", key='PdID_Delete', min_value=1, step=1)
    if st.button("刪除商品"):
        delete_product(id)
    

# 在側邊欄添加選項
menu = ['首頁', '客戶端', '企業方']
choice = st.sidebar.selectbox('選擇你要前往的頁面', menu)

# 添加回到首頁的按鈕
if st.button('首頁'):
    choice = '首頁'

# 根據使用者的選擇顯示不同的頁面
if choice == '首頁':
    st.header("購物車系統")
    st.write('歡迎來到購物車系統！')
    st.write('請在左方側邊欄選擇您是 "客戶" 或 "企業" ')
elif choice == '客戶端':
    customer_page()
elif choice == '企業方':
    company_page()





