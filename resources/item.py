from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This fiels can not be blank!"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found"}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exists,".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)                 #like, item = ItemModel(name, data['price'], data['store_id'])
        """
        conn = sqlite3.connect()
        cursor = conn.cusrsor()

        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item['name'],item['price']))

        conn.commit()
        conn.close()
        """
        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item"}, 500  #server error
        return item.json(), 201


    # delete item

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "Item deleted"}

    def put(self, name):

        data = Item.parser.parse_args()

        """
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
        """
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)  #like, item = ItemModel(name, data['price'], data['store_id'])


        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.find_all()]}
