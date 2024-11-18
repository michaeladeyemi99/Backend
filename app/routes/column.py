from flask import Blueprint, request
from flask_restful import Resource, Api
from app import db
from app.models import Column


column_bp = Blueprint("api_column", __name__)
column_api = Api(column_bp)

class ColumnGet(Resource):
    # Handle GET requests for a specific column by ID
    def get(self, column_id):
        try:
            column = db.get_or_404(Column, column_id)
            return {
                "column_id": column.column_id,
                "column_name": column.column_name,
                "column_order_id": column.column_order_id,
                "board_id": column.board_id
            }
        except Exception as e:
            return {"error": "There is an error getting the column"}, 500


class ColumnPost(Resource):
    # Handle POST requests for creating a new column
    def post(self):
        try:
            # Get data from request JSON
            data = request.json
            column_name = data.get("column_name")
            column_order_id = data.get("column_order_id")
            board_id = data.get("board_id")

            # Create a new column instance
            column = Column(column_name=column_name, column_order_id=column_order_id , board_id=board_id)
            db.session.add(column)
            db.session.commit()

            return {
                "column_id": column.column_id,
                "column_name": column.column_name,
                "column_order_id": column_order_id,
                "board_id": column.board_id
            }, 201
            
        except Exception as e:
            return {"error": f"There is an error posting the column {e}"}, 500


class ColumnDelete(Resource):
    def delete(self, column_id):
        try:
            column = db.session.execute(db.select(Column).filter_by(column_id = column_id)).scalar_one()

            db.session.delete(column)
            db.session.commit()

            return(
                {
                    "Success" : f"Successfully deleted {column_id}"
                }
            ), 200
        except Exception as e:
            return (
                {"error" : f"Could not delete the id {column_id}{e}"}
            ), 500


class ColumnPatch(Resource):
    def patch(self, column_id):
        data = request.json
        column_name = data.get("column_name")
        column_order_id = data.get("column_order_id")
        board_id = data.get("board_id")
        try:
            column =  db.session.execute(db.select(Column).filter_by(column_id = column_id)).scalar_one()
            column.column_name = column_name
            column.column_order_id = column_order_id
            column.board_id = board_id
            db.session.commit()
            return(
                {
                    "Success" : f"You have edited the id {column_id}"
                }
            ), 200
        except Exception as e:
            return(
                {
                    "error" : f"There was an error with patching {column_id} {e}"
                }
            ), 500

# Register the resources with distinct routes
column_api.add_resource(ColumnGet, '/columns/<int:column_id>', endpoint="get_column")
column_api.add_resource(ColumnPost, '/columns', endpoint="post_column")
column_api.add_resource(ColumnDelete, '/columns/<int:column_id>', endpoint="delete_column")
column_api.add_resource(ColumnPatch, "/columns/<int:column_id>", endpoint="patch_column")