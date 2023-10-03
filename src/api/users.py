from flask import Blueprint, jsonify, abort, request
from ..models import User, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()



bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods= ['GET'])
def index():
    users = User.query.all()
    result = []
    for u in users:
        result.append(u.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id, "User not found")
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and 
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if len(username) < 3 or len(password) < 8:
        return abort(400)
    # user with id of user_id must exist

    # construct User
    u = User(username=username, email=email, password_hash=scramble(password))
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(u.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id):
    u = User.query.get_or_404(id)

    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    
    username = request.json.get('username')  # Use get() to safely retrieve values
    password = request.json.get('password')  # Use get() to safely retrieve values

    if 'username' in request.json and len(username) < 3:
        return abort(400)

    if 'password' in request.json and len(password) < 8:
        return abort(400)
    
    if 'username' in request.json:
        u.username = username

    if 'password' in request.json:
        u.password = scramble(password)

    try:
        db.session.commit()  
        return jsonify(u.serialize())
    except:
        return jsonify(False)

    
