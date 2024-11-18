from flask import Blueprint, request
from flask_restful import Resource, Api
from app import db
from app.models import Board


board_bp = Blueprint("api_board", __name__)
board_api = Api(board_bp)

class BoardGet(Resource):
    # Handle GET requests for a specific board by ID
    def get(self, board_id):
        try:
            board = db.get_or_404(Board, board_id)
            return {
                "board_id": board.board_id,
                "board_name": board.board_name,
                "user_id": board.user_id
            }
        except Exception as e:
            return {"error": "There is an error getting the board"}, 500

class BoardPost(Resource):
    # Handle POST requests for creating a new board
    def post(self):
        try:
            # Get data from request JSON
            data = request.json
            board_name = data.get("board_name")
            user_id = data.get("user_id")

            # Create a new board instance
            board = Board(board_name=board_name, user_id=user_id)
            db.session.add(board)
            db.session.commit()

            return {
                "board_id": board.board_id,
                "board_name": board.board_name,
                "user_id": board.user_id
            }, 201
            
        except Exception as e:
            return {"error": "There is an error posting the board"}, 500


class BoardDelete(Resource):
    def delete(self, board_id):
        try:
            board = db.session.execute(db.select(Board).filter_by(board_id = board_id)).scalar_one()

            db.session.delete(board)
            db.session.commit()

            return(
                {
                    "Success" : f"Successfully deleted {board_id}"
                }
            ), 200
        except Exception as e:
            return (
                {"error" : f"Could not delete the id {board_id}{e}"}
            ), 500


class BoardPatch(Resource):
    def patch(self, board_id):
        data = request.json
        board_name = data.get("board_name")
        try:
            board =  db.session.execute(db.select(Board).filter_by(board_id = board_id)).scalar_one()
            board.board_name = board_name
            db.session.commit()
            return(
                {
                    "Success" : f"You have edited the id {board_id}"
                }
            ), 200
        except Exception as e:
            return(
                {
                    "error" : f"There was an error with patching {board_id} {e}"
                }
            ), 500

class GetUserBoards(Resource):
    def get(self, user_id):
        boards = db.session.execute(db.select(Board).filter_by(user_id=user_id)).scalars()
        
        board_list = []

        for board in boards:
            board_data = {
                "board_id" : board.board_id,
                "board_name" : board.board_name,
                "board_user_id": board.user_id
            }
            board_list.append(board_data)
        
        return board_list

# Register the resources with distinct routes
board_api.add_resource(BoardGet, '/boards/<int:board_id>', endpoint="get_board")
board_api.add_resource(BoardPost, '/boards', endpoint="post_board")
board_api.add_resource(BoardDelete, '/boards/<int:board_id>', endpoint="delete_board")
board_api.add_resource(BoardPatch, "/boards/<int:board_id>", endpoint="patch_board")
board_api.add_resource(GetUserBoards, "/<int:user_id>/boards", endpoint="get_user_boards")
