from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from app import db
from app.models import User


user_bp = Blueprint("api_user", __name__)
user_api = Api(user_bp)

class UserGet(Resource):
    # Handle GET requests for a specific user by ID
    def get(self, user_id):
        try:
            user = db.get_or_404(User, user_id)
            return {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_UID": user.user_UID
            }
        except Exception as e:
            return {"error": "There is an error getting the user"}, 500


class UserPost(Resource):
    # Handle POST requests for creating a new user
    def post(self):
        try:
            # Get data from request JSON
            data = request.json
            user_name = data.get("user_name")
            user_email = data.get("user_email")
            user_UID = data.get("user_UID")
            if not user_name or not user_UID or not user_email:
                return {"error": "user_name, user_email and user_UID are required fields"}, 400

            # Create a new user instance
            user = User(user_name=user_name, user_email=user_email, user_UID=user_UID)
            db.session.add(user)
            db.session.commit()

            return {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_UID": user.user_UID
            }, 201
            
        except Exception as e:
            return {"error": "There is an error posting the user"}, 500

class GetAllUsersUIDs(Resource):
    def get(self):
        try:
            users = db.session.execute(db.select(User).order_by(User.user_id)).scalars()
            user_list = []
            for row in users:
                user_data = {
                    "user_id": row.user_id,
                    "user_name": row.user_name,
                    "user_email": row.user_email,
                    "user_UID": row.user_UID
                }
                user_list.append(user_data)
            return {"users": user_list},200
        except Exception as e:
            return{"error" : f"Data not Fetched {e}"}, 404
         


# Register the resources with distinct routes
user_api.add_resource(UserGet, '/users/<int:user_id>', endpoint="get_user")
user_api.add_resource(UserPost, '/users', endpoint="post_user")
user_api.add_resource(GetAllUsersUIDs, '/users/getallusers', endpoint="getallusersIDs")