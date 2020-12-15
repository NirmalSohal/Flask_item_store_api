import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a store id."
    )


    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        return {'message':f'The item with name: {name} does not exists'},400
    

    def post(self,name):
        row=ItemModel.find_by_name(name)
        if row:
            return {'message':f'The item with name: {name} already exists'},400
        else:
            data=Item.parser.parse_args()
            item=ItemModel(name,data['price'],data['store_id'])
            try:
                item.save_to_db()
                return item.json(),200
            except:
                return {'message':'An internal error occured while inserting the item'},500

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return item.json()
        else:
            return{'message':f'item with name: {name} not found'},404

    def put(self,name):
        item=ItemModel.find_by_name(name)
        data=Item.parser.parse_args()
        if item is None:
            item=ItemModel(name,data['price'],data['store_id'])
        else:
            item.price=data['price']
        
        item.save_to_db()
        return item.json()

    

class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
