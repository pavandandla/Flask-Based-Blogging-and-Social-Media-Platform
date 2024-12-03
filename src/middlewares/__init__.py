from functools import wraps
import jwt
import os
import logging
from flask import request, jsonify, Response, g
#from config.config import Config
from models.all_models import User, Post
from config.database import db
from dotenv import load_dotenv

def decode_jwt(token):
    try:
        token = token.split(" ")[1]  # Split the token in 'Bearer <token>' format
        return jwt.decode(token, str(os.getenv('SECRET_KEY')), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        return {'error': 'Invalid token'}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.warning("Missing Authorization header")
            return Response(
                response='{"message": "Unauthorized - Missing Authorization header"}',
                status=401
            )
        try:
            data = decode_jwt(token)
            if 'error' in data:
                print("error ra mama")
                return Response(
                    response=f'{{"message": "Unauthorized - {data["error"]}"}}',
                    status=401
                )
            
            current_user = User.query.filter_by(id=int(data['id'])).first()
           
        except:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not hasattr(current_user, 'role') or current_user.role != 'admin':
            logging.warning("User is not authorized")
            return Response(
                response='{"message": "Unauthorized - User is not authorized"}',
                status=403
            )
        return f(current_user, *args, **kwargs)
    return decorated

def user_or_admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not hasattr(current_user, 'role'):
            logging.warning("User is not authorized")
            return Response(
                response='{"message": "Unauthorized - User is not authorized"}',
                status=403
            )
        return f(current_user, *args, **kwargs)
    return decorated