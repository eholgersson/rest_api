import numpy as np
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=False)

        args = parser.parse_args()

        data = pd.read_csv(filename_usr, encoding='utf-8')
        
        if args['userId'] != None:
            print(args['userId'])
            data = data[data['userId'] == args['userId']]

            data = data.to_dict()
            return {'data': data}, 200
        
        else:
            #print('in else')
            data = data.to_dict()
            return {'data': data}, 200

    def post(self):
        # write to db

        # read our csv
        data = pd.read_csv(filename_usr, encoding='utf-8')

        if request.form['userId'] in list(data['userId']):
            return {
                'message' : f"'{request.form['userId']}' already exists."
            }, 401

        else:
            # create df of new data
            new_data = pd.DataFrame({
                'userId' : request.form['userId'],
                'name' : request.form['name'],
                'city' : request.form['city'],
                'locations': [[]]
            })

            # append the new data
            data = data.append(new_data, ignore_index=True)
            
            # write back to "database"
            data.to_csv(filename_usr, encoding='utf-8', index=False)

            return {'data':data.to_dict()}, 200


    def put(self):
            
        data = pd.read_csv(filename_usr, encoding='utf-8')
        #return {'body':request.form}
        if request.form['userId'] in list(data['userId']):
            
            # evaluate strings of list to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )            

            # select our user
            user_data = data[data['userId']==request.form['userId']]

            if request.form['locations'] in list(user_data['locations'].values[0]):
                return {
                    'message' : f"locations already added for user '{request.form['userId']}"
                }

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0].append(request.form['locations'])

            # write back to "database"
            data.to_csv(filename_usr, encoding='utf-8', index=False)

            return {'data': data.to_dict()}, 200
        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{request.form['userId']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=True)

        args = parser.parse_args()
        
        data = pd.read_csv(filename_usr, encoding='utf-8')
         
        if args['userId'] not in list(data['userId']):
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404
        else:

            data = data[data['userId'] != args['userId']]
            data.to_csv(filename_usr, encoding='utf-8', index=False)

            return {'data': data.to_dict()}, 200


class Locations(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=False, type=int)

        args = parser.parse_args()

        data = pd.read_csv(filename_loc, encoding='utf-8')
        
        if args['locationId'] != None:
            print(args['locationId'])
            data = data[data['locationId'] == args['locationId']]

            data = data.to_dict()
            return {'data': data}, 200
        
        else:
            #print('in else')
            data = data.to_dict()
            return {'data': data}, 200
    
    def post(self):

        data = pd.read_csv(filename_loc, encoding='utf-8')
        loc_id = int(request.form['locationId'])
        
        if loc_id in list(data['locationId']):
            return {
                'message' : f"'{loc_id}' location already exists" 
            }, 401

        else:
            
            new_data = pd.DataFrame({
                'locationId': [loc_id], 
                'name': request.form['name'], 
                'rating': float(request.form['rating'])
            })

            data = data.append(new_data, ignore_index=True)

            data.to_csv(filename_loc, encoding='utf-8', index=False)
            
            return {'data':data.to_dict()}, 200


    def patch(self):
        data = pd.read_csv(filename_loc, encoding='utf-8')
        
        loc_id = int(request.form['locationId'])

        if loc_id in list(data['locationId']):
            user_data = data[data['locationId']==loc_id]

            if 'name' in request.form:
                user_data['name'] = request.form['name']
            
            if 'rating' in request.form:
                user_data['rating'] = float(request.form['rating'])

            data[data['locationId'] == loc_id] = user_data

            data.to_csv(filename_loc, encoding='utf-8', index=False)

            return {'data': data.to_dict()} , 200
        
        else:
            return {
                'message' : f"'{request.form['locationId']}' locataion does not exist."
            },404
    
    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True, type=int) # id of locations to delete
        args = parser.parse_args()

        data = pd.read_csv(filename_loc, encoding='utf-8')
        
        if args['locationId'] not in list(data['locationId']):
            return {
                'message': f"'{args['locationId']}' location not found."
            }, 404
        else:
            data = data[data['locationId'] != args['locationId']]
            data.to_csv(filename_loc, encoding='utf-8', index=False)
            
            return {'data': data.to_dict()}, 200 


class Default(Resource):
    def get(self):
        #data = pd.read_csv('locations.csv')

        return {
            'message':f"Default message 1, name of script: '{__name__}'"
            }, 200


def main():
    #print('in main')
    global filename_usr, filename_loc
    path = os.getcwd()
    filename_usr = path + '/users.csv'
    filename_loc = path + '/locations.csv'

    api.add_resource(Users, '/users') # '/users' is our entry point
    api.add_resource(Locations, '/locations')  # '/locations' is our entry point

    api.add_resource(Default, '/')  # '/' is our default entry point


main()
#print(__name__)
app.run()

# TODO: Try to export app.run() and run through cmd command: python3 -m flask run in docker
#if __name__ == '__main__':
    #main()

    #app.run()  # run our Flask app