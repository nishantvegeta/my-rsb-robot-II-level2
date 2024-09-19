from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
import os

# Initialize the libraries
http = HTTP()
table_module = Tables()
pdf_lib = PDF()

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    """
    # browser.configure(slowmo=100)
    open_robot_order_website()
    close_annoying_modal()
    download_orders_file()
    orders = get_orders()
    browser.close_browser()

def open_robot_order_website():
    """Opens the RobotSpareBin Industries robot order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def close_annoying_modal():
    """Close the 'OK' modal popup on the website"""
    page = browser.page()
    page.click("button:text('OK')")
    
def download_orders_file():
    """Download the orders CSV file from the website"""
    url = "https://robotsparebinindustries.com/orders.csv"
    http.download(url, overwrite=True, target_file="orders.csv")

def get_orders():
    """Read the orders CSV file and return it as a table"""
    orders_table = table_module.read_table_from_csv("orders.csv")
    print(f"Orders Table: {orders_table}")
    process_orders(orders_table)


def process_orders(orders):
    """Process each order from the CSV"""
    for order in orders:
        print(f"Processing Order: {order}")
        fill_the_form(order)
       

def fill_the_form(order):
    page=browser.page()
    """Fill out the robot order form based on the order details"""

    page.select_option("#head",str(order["Head"]))

    path = f"//input[@type='radio' and @name='body' and @value={order['Body']} ]"
    page.click(path)



    page.fill('//*[@class="form-control"][1]',order['Legs'])
    page.fill("#address",order["Address"])

    page.click("button:text('Order')")