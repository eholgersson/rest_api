import numpy as np
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv(filename_usr, encoding='utf-8')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        # write to db

        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args() # parse arguments to dict

        # read our csv
        data = pd.read_csv(filename_usr, encoding='utf-8')

        if args['userId'] in list(data['userId']):
            return {
                'message' : f"'{args['userId']}' already exists."
            }, 401
        else:
            # create df of new data
            new_data = pd.DataFrame({
                'userId' : args['userId'],
                'name' : args['name'],
                'city' : args['city'],
                'locations': [[]]
            })  

            # append the new data
            data = data.append(new_data, ignore_index=True)
            
            # write back to "database"
            data.to_csv(filename_usr, encoding='utf-8', index=False)

            return {'data':data.to_dict()}, 200

    def put(self):
        
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args() # parse arguments to dict

        data = pd.read_csv(filename_usr, encoding='utf-8')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of list to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )

            # select our user
            user_data = data[data['userId']==args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

            # write back to "database"
            data.to_csv(filename_usr, encoding='utf-8', index=False)

            return {'data': data.to_dict()}, 200
        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
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
        data = pd.read_csv(filename_loc, encoding='utf-8')
        data = data.to_dict()    
        return {'data': data}, 200
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('rating', required=True)
        args = parser.parse_args()

        data = pd.read_csv(filename_loc, encoding='utf-8')

        if args['locationId'] in list(data['locationId']):
            return {
                'message' : f"'{args['locationId']}' already exists" 
            }, 401

        else:
            print('inne i elsen')
            print(type(args['locationId']))
            new_data = pd.DataFrame({
                'locationId': args['locationId'], 
                'name': args['name'], 
                'rating': args['rating']
            })

            data = data.append(new_data, ignore_index=True)

            data.to_csv(filename_loc, encoding='utf-8', index=False)
            
            return {'data':data.to_dict()}, 200


    def patch(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', required=False)
        parser.add_argument('rating', required=False)
        args = parser.parse_args()

        data = pd.read_csv(filename_loc, encoding='utf-8')
        
        if args['locationId'] in list(data['locationId']):
            user_data = data[data['locationId']==args['locationId']]

            if 'name' in args:
                user_data['name'] = args['name']
            
            if 'rating' in args:
                user_data['rating'] = args['rating']

            data[data['locationId'] == args['locationId']] = user_data

            data.to_csv(filename_loc, encoding='utf-8', index=False)

            return {'data': data.to_dict()} , 200
        
        else:
            return {
                'message' : f"'{args['locationId']}' locataion does not exist."
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

# TODO: Try to export app.run() and run through cmd command: python3 -m flask run in docker
#if __name__ == '__main__':
    #main()

    #app.run()  # run our Flask app