from flask import Blueprint, jsonify, abort, request
from ..models import Post, User, db

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('', methods= ['GET'])
def index():
    posts = Post.query.all()
    result = []
    for p in posts:
        result.append(p.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Post.query.get_or_404(id, "Post not found")
    return jsonify(p.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'date' not in request.json or 'image' not in request.json or 'caption' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'], "User not found")
    # construct Post
    p = Post(
        user_id=request.json['user_id'],
        date=request.json['date'],
        image=request.json['image'],
        caption=request.json['caption']
    )
    db.session.add(p) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(p.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Post.query.get_or_404(id, "Post not found")
    try:
        db.session.delete(p) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


