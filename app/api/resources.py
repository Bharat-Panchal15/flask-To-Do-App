from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app.extensions import db
from app.utils import success_response, error_response

parser = reqparse.RequestParser()
parser.add_argument("title",type=str,required=True,help="Title is required")
parser.add_argument("done",type=bool,default=False)

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())

        done_filter = request.args.get("done")
        page = request.args.get("page",1,type=int)
        limit = request.args.get("limit",5,type=int)
        
        query = Task.query.filter_by(user_id=current_user_id)

        if done_filter is not None:
            done = done_filter.lower() == 'true'
            query = query.filter_by(done=done)
        
        paginated = query.paginate(page=page,per_page=limit,error_out=False)

        data = {
            "tasks":[task.to_dict() for task in paginated.items],
            "page":paginated.page,
            "pages":paginated.pages,
            "total_tasks":paginated.total
        }


        return success_response(data)
    
    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())

        args = parser.parse_args()

        new_task = Task(title=args['title'],done=args['done'],user_id=current_user_id)
        db.session.add(new_task)
        db.session.commit()
        
        return success_response(new_task.to_dict(),201)
    
    @jwt_required()
    def put(self,task_id):
        current_user_id = int(get_jwt_identity())

        task = Task.query.filter_by(id=task_id,user_id=current_user_id).first()

        if task is None:
            return error_response(f"Task with task ID: {task_id} not found or unauthorized.")
        
        args = parser.parse_args()

        task.title = args['title']
        task.done = args['done']

        db.session.commit()


        return success_response(task.to_dict())
    
    @jwt_required()
    def delete(self,task_id):
        current_user_id = int(get_jwt_identity())

        task = Task.query.filter_by(id=task_id,user_id=current_user_id).first()

        if task is None:
            return error_response(f"Task with task ID: {task_id} not found or unauthorized.")

        db.session.delete(task)
        db.session.commit()


        return success_response(data=task.to_dict(),message=f"Task with task ID: {task_id} deleted successfully.")