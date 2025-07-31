from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import User
from app.extensions import db
from app.utils import success_response, error_response
from app.models import BlackListedToken

# register_parser = reqparse.RequestParser()
# register_parser.add_argument("username", type=str, required=True, help="Username is required.")
# register_parser.add_argument("password", type=str, required=True, help="Password id required.")

class RegisterResource(Resource):
    def post(self):
        # args = register_parser.parse_args()
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return error_response(message="Missing fields",status=400)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return error_response(message="Username already taken.",status=400)
        
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return success_response({"username":username,"message":"Data received"},201)
    
login_parser = reqparse.RequestParser()
login_parser.add_argument("username",type=str,required=True,help="Username is required.")
login_parser.add_argument("password",type=str,required=True,help="Password is required.")

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return error_response("Invalid username or password.",status=401)
        
        token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return success_response({
            "access_token":token,
            "refresh_token": refresh_token
        })

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)

        return success_response({'access_token': new_access_token})
    
class LogoutResource(Resource): 
    def post(self):
        data = request.json
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return error_response(message="Refresh token is required.",status=400)
        
        blacklisted_token = BlackListedToken(token=refresh_token)

        db.session.add(blacklisted_token)
        db.session.commit()
        return success_response(message="Logged out successfully")