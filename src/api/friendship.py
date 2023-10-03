from flask import Blueprint, jsonify, abort, request
from ..models import Post, Friendship, User, db

bp = Blueprint('friendship', __name__, url_prefix='/friendship')

@bp.route('', methods= ['GET'])
def index():
    friendship = Friendship.query.all()
    result = []
    for f in friendship:
        result.append(f.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    f = Friendship.query.get_or_404(id, "Friendship not found")
    return jsonify(f.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id1 and user_id2
    if 'user_id1' not in request.json or 'user_id2' not in request.json or 'status' not in request.json or 'created_at' not in request.json:
        return abort(400)
    # user with id of user_id1 and user_id2 must exist
    User.query.get_or_404(request.json['user_id1'], "User not found")
    User.query.get_or_404(request.json['user_id2'], "User not found")
    # construct Friendship
    f = Friendship(
        user_id1=request.json['user_id1'],
        user_id2=request.json['user_id2'],
        status=request.json['status'],
        created_at=request.json['created_at'],
    )
    db.session.add(f) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(f.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    f = Friendship.query.get_or_404(id, "Friendship not found")
    try:
        db.session.delete(f) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

