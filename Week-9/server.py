from flask import Flask
import json
app = Flask(__name__)

@app.route('/') # the home route
def index ():
    return 'hello world'

#create another sub route

@app.route('/hello')
def say_hello():
    return 'hey there!'

#use a route parameter
@app.route('/<name>')
def say_hello_with_name(name):
    return f'hey there {name}'

@app.route('/classmates')
def get_classmates():
    return {"response_code": 200, "data": ['dan', 'pavel', 'enzo', 'son', 'priscilla', 'Sanjeev']}

#implement a route that reutnrs the classmate that matches an id 
#create a list of dictionaries, with each name having an id



@app.route('/classmates/<id>')
def get_classmate(id):
    names = [{'id':1, 'name':'dan'}, {'id':2, 'name':'priscilla'}, {'id':3, 'name':'ella'}, {'id':4, 'name':'enzo'}]
    names_object = json.dumps(names, indent = 4)

    for item in names:
        if item['id'] ==int(id):
            return item
  
    return {"response_code": 404} 



    #return {"response_code":200, "data": names['id']}

if __name__ == '__main__':
    app.run()
