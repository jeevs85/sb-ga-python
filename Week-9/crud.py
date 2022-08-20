#crud application for products in a store

#what are we storing about products
# inventory_level * (we may want to store this separately)
# name
# description
# id
# price
#id,name,description,price (products.csv)

#create a product


#read product data

#update a product

#delete a product


from crypt import methods
from select import select
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
#from flask_bootstrap import Bootstrap
import json

#create a flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

#route to dispaly all products
@app.route('/products')
def get_products(): #list all the products
    #read my products file
    product_list = pd.read_csv('products.csv')
    return render_template('products.html', products=product_list.to_dict('records'))

#route to add a new product
@app.route('/products/new', methods=['GET', 'POST'])
def add_new_product():
    if request.method == 'GET':
        return render_template('new-product.html')
    else:
        #read the current products from file file
        products = pd.read_csv('products.csv')
        product_list = products.to_dict('records')

        #add new product to list
        product_name = request.form['name']
        product_desc = request.form['description']
        product_price = request.form['price']
        new_product = {}

        new_product_id = product_list[len(product_list) - 1]['id'] + 1

        new_product['id'] = new_product_id
        new_product['name'] = product_name
        new_product['description'] = product_desc
        new_product['price'] = product_price

        product_list.append(new_product)

        #write updated list to file

        df = pd.DataFrame(product_list).set_index('id') 
        df.to_csv('products.csv')
        return redirect(url_for('get_products'))

#route to edit each product
@app.route('/products/<id>', methods=["GET", "PUT", "POST"])
def edit_product(id):
    #1. read the list products from the csv file
    product_list = fetch_product_list()
    #2. find the product that matches the given id
    selected_product = None
    for product in product_list:
        if product['id'] == int(id):
            selected_product = product
            break
    #if it is a GET request, show the form with the data filled out in the form fields
    if request.method == 'GET':
        #return the edit-product template
        return render_template('edit-product.html', product=selected_product)
    
    else:
        data = {
            'id': product['id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'price': request.form['price']
        }
        #update product list by replacing existing product with updated one
        #again, search for the one with matching id
        update_product(product_list, data)
        #write the changes to the file
        df = pd.DataFrame(product_list).set_index('id')
        df.to_csv('products.csv')
        return redirect(url_for('get_products'))

@app.route('/products/<id>/delete', methods=['POST','DELETE'])
def delete_product(id):
    delete_product(request.form['delete'])
    return redirect(url_for('get_products'))


def fetch_product_list():
    products = pd.read_csv('products.csv')
    return products.to_dict('records')

def update_product(product_list, new_product):
    for idx in range(len(product_list)):
        if new_product['id'] == product_list[idx]['id']:
            product_list[idx] = new_product
            break

def delete_product(id):
    product_list = fetch_product_list()
    new_list = [product for product in product_list if not (product['id'] == int(id)) ]
    df = pd.DataFrame(new_list).set_index('id')
    df.to_csv('products.csv')


if __name__ == '__main__':
    app.run(debug=True)