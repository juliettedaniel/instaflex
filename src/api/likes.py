from flask import Blueprint, jsonify, abort, request
from ..models import User, Like, Post, db

bp = Blueprint('likes', __name__, url_prefix='/likes')

@bp.route('', methods= ['GET'])
def index():
    likes = Like.query.all()
    result = []
    for l in likes:
        result.append(l.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = Like.query.get_or_404(id, "Likes not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and post_id
    if 'user_id' not in request.json or 'post_id' not in request.json:
        return abort(400, "The user_id and post_id fields are required")
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'], "User not found")
    Post.query.get_or_404(request.json['post_id'], "Post not found")
    # construct Likes
    l = Like(
        user_id=request.json['user_id'],
        post_id=request.json['post_id'],
    )
    db.session.add(l) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = Like.query.get_or_404(id, "Likes not found")
    try:
        db.session.delete(l) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify({"success": False, "message": "An error occurred while deleting the like."})

