from flask import Blueprint
from flask_restful import Api
from .resources import TaskListResource
from .auth_resources import RegisterResource, LoginResource, RefreshTokenResource, LogoutResource

api_bp = Blueprint('api',__name__)
api = Api(api_bp)
api.add_resource(TaskListResource, "/tasks", "/tasks/<int:task_id>")
api.add_resource(RegisterResource,"/register")
api.add_resource(LoginResource,"/login")
api.add_resource(RefreshTokenResource, "/refresh")
api.add_resource(LogoutResource,"/logout")