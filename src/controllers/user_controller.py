
from flask import request, Response, json, jsonify, g
from services import user_role_service
from middlewares import token_required, admin_required , user_or_admin_required
from models.all_models import User, Post
# @authenticate_admin
def signup():
    #user_info = g.get('user_info')  # Extract user info if needed from middleware
    data = request.form
    response, status = user_role_service.signup(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json') #mimetype='application/json'

def login():
    data = request.form
    response, status = user_role_service.login(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

def logout():
    user_info = g.get('user_info')  # Authenticated user info
    response, status = user_role_service.logout(user_info)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')
  
@token_required
@admin_required
def get_userdata(current_user):
    #user_info = g.get('user_info')  # Authenticated user info
    #data = request.form
    response, status = user_role_service.get_userdata()
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

# task:6 controllers
@token_required
def create_post(current_user):
    data = request.form
    response, status = user_role_service.create_post(current_user,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def get_post(current_user):
    response, status = user_role_service.get_post(current_user)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def update_post(current_user,post_id):
    post_id=post_id
    data=request.form
    response, status = user_role_service.update_post(current_user,post_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def delete_post(current_user, post_id):
    """
    Deletes a post by ID after user authentication.
    """
    # Call service to delete the post
    post_id=post_id
    response, status = user_role_service.delete_post(current_user,post_id)  # Use post_id directly
    
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def create_comment(current_user):
    data = request.form
    post_id=data['post_id']
    user_id=current_user.id
    response, status = user_role_service.create_comment(user_id,post_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def get_comment(current_user,post_id):
    response, status = user_role_service.get_comment(current_user,post_id)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def update_comment(current_user,comment_id):
    # Authenticated user info
    data = request.form   
    post_id=data['post_id']
    response, status = user_role_service.update_comment(current_user,comment_id,post_id, data)  # Call service function
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def delete_comment(current_user,comment_id):  
    data = request.form   
    post_id=data['post_id']
    response, status = user_role_service.delete_comment(current_user,comment_id,post_id)  # Use post.id
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def create_like(current_user):
    data = request.form
    post_id=data['post_id']
    user_id=current_user.id
    response, status = user_role_service.create_like(user_id,post_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def update_like(current_user,like_id):
    # Authenticated user info
    data = request.form   
    post_id=data['post_id']
    response, status = user_role_service.update_like(current_user,like_id,post_id, data)  # Call service function
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@user_or_admin_required
def delete_like(current_user,like_id):  
    data = request.form   
    post_id=data['post_id']
    response, status = user_role_service.delete_like(current_user,like_id,post_id)  # Use post.id
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

#task 18 related work

@token_required
def follow(current_user, target_id):
    follower_id= current_user.id
    followed_id= target_id
    response, status = user_role_service.follow_user(follower_id, followed_id)  
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def unfollow(current_user, target_id):
    follower_id= current_user.id
    followed_id= target_id
    response, status = user_role_service.unfollow_user(follower_id, followed_id)  
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def notification(current_user):
    response, status = user_role_service.notification_user(current_user)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')
