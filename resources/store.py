from models.store import StoreModel
from flask_restful import Resource, reqparse

class Store(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('item id',
        type=int,
        required=True,
        help="Please provide the name of the store"

    )
    def get(self,name):
        store_found=StoreModel.find_by_name(name)
        if store_found:
            return store_found.json()
        else:
            return {'message':'Store not found'},404
    
    def post(self,name):
        store_found=StoreModel.find_by_name(name)
        if store_found:
            return {'message':f'Store with name: {name} already exists.'},404
        else:
            #data=Store.parser.parse_args()
            store=StoreModel(name)
            store.save_to_db()
            return store.json()
    
    def delete(self,name):
        store_found=StoreModel.find_by_name(name)
        if store_found:
            store_found.delete_from_db()
        
        return {'message':'Deleted'}


class StoreList(Resource):
    def get(self):
        return {'Stores':[store.json() for store in StoreModel.query.all()]}
