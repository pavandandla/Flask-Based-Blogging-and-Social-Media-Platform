from models.all_models import User, db, Post, Comment, Post_Like, Follower, Notification
from flask import current_app
from flask import request
import jwt
from config.config import bcrypt
import os
from dotenv import load_dotenv 

def create_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()
    return notification

def signup(data):#,user_ifo
    try:
        if "username" in data and "email" in data and "password" in data:
            username = data["username"]
            email = data["email"]
            password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

            role = data.get("role", "user")  # Defaults to 'user' if 'role' is not provided
            
            
            # Create a new user object
            new_user = User(username=username, email=email, password=password,role=role)  # Hash password before saving!
            
            db.session.add(new_user)
            db.session.commit()
            return {'status': "success", "statusCode": 201, "message": "User created successfully!"}, 201
        else:
            return {'status': "failed", "statusCode": 400, "message": "Username, email, and password are required"}, 400
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500
    
def login(data):
    try:
        if "email" in data and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user and bcrypt.check_password_hash(user.password, data["password"]):
                # Include role and username in the token
                token_Data = {
                    'role': user.role,
                    'username': user.username,
                    'id': user.id
                }
                #print("id===>",user.id)
                
                # Encode the token using JWT
                token = jwt.encode(token_Data, str(os.getenv('SECRET_KEY')) , algorithm='HS256')

                return {'message':f"Login Successful.Welcome,{user.username}!", 'status': "success", "statusCode": 200, "token": token}, 200
            else:
                return {'status': "failed", "statusCode": 401, "message": "Invalid credentials!"}, 401
        else:
            return {'status': "failed", "statusCode": 400, "message": "Email and password are required"}, 400
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500


def get_userdata():
    try:
        # Retrieve all users
        users = User.query.all()

        if not users:
            return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404

        # Use the custom to_dict method in the User model to serialize users, posts, and comments
        user_data = [user.user_to_dict() for user in users]  # Serialize all users with their posts and comments

        return {'status': "success", "statusCode": 200, "data": user_data}, 200  # Return user data as JSON

    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error retrieving user data", "error": str(e)}, 500

# @log_function_execution
def logout(user_info):
    try:
        # Normally, the frontend will handle removing the JWT token.
        return {'status': "success", "statusCode": 200, "message": "Logged out successfully!"}, 200
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500
    
#task 9:related work

def create_post(current_user,data):
    user = User.query.filter_by(id=current_user.id).first()
    if not user:
        return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404  # Handle no users case
    else:
        if Post.query.filter_by(title=data['title']).first():
            return {'status': "failed", "statusCode": 400, "message": "Title is already in use"}, 400
        else:
            new_post = Post(title=data['title'], content=data['content'], owner=user)
            db.session.add(new_post)
            db.session.commit()
            return {'status': "success", "statusCode": 201, "message": "Post created successfully"}, 201
   
# Get all posts
def get_post(current_user):
    post = Post.query.filter_by().all()

    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Posts not found"}, 404 
    if current_user.role=='admin' or current_user.id == post[0].owner_id:
            
    # Use the schema to serialize the post, including its comments
            post_data = [pos.post_to_dict() for pos in post]
            return {
                'status': "success",
                "statusCode": 200,
                "message":"See the posts ",
                "data": post_data }, 200
    
    else:
        
        return {'status': "failed", "statusCode": 403,"message": "Permission denied due to not a admin or postowner"}, 403
        

def update_post(current_user,post_id,data):
    post = Post.query.filter_by(id=post_id).first()
        
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Posts not found"}, 404 
    if current_user.role=='admin' or current_user.id == post.owner_id:
      
        if Post.query.filter_by(title=data['title']).first():
                return {'status': "failed", "statusCode": 400, "message": "Title is already in use"}, 400
        else:
            post.title = data['title']
            post.content = data['content']
            db.session.commit()
            return  {'status': "success", "statusCode": 200, "message": "Post updated successfully"}, 200
    else:
        return {'status': "failed", "statusCode": 403,"message": "Permission denied due to not a admin or postowner"}, 403

    

def delete_post(current_user,post_id):
    """
    Deletes a post from the database.
    """
    try:
        post = Post.query.get_or_404(post_id)  # Retrieve post by ID or return 404 if not found
        if not post:
           return {'status': "failed", "statusCode": 404, "message": "Posts not found"}, 404 
        if current_user.id == post.owner_id or current_user.role=='admin':
             db.session.delete(post)  # Delete the post from the session
             db.session.commit()  # Commit the changes to the database
             return {'status': "success", "statusCode": 200, "message": "Post deleted successfully"}, 200
        else:
            return {'status': "failed", "statusCode": 403,"message": "Permission denied due to not a admin or postowner"}, 403
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return {'status': "failed", "statusCode": 500, "message": "Error deleting post", "error": str(e)}, 500
    

def create_comment(user_id,post_id,data):
    user = User.query.filter_by(id=user_id).first()
    if not user:
         return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404
    user_id=user.id
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "No posts found"}, 404  # Handle no users case
    
    new_comment = Comment(comment=data['comment'],user_id=user_id, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    create_notification(post.owner_id, f"User {user_id} commented on your post.")
    return {'status': "success", "statusCode": 201, "message": "Comment created successfully"}, 201

def get_comment(current_user,post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id).all()
        print("comments:",comments)
        if not comments:
            return {'status': "failed", "statusCode": 404, "message": "No comments found"}, 404

        # Use CommentSchema to serialize the comments
        comment_data = [comment.comment_to_dict() for comment in comments]

        return {'status': "success", "statusCode": 200, "message": "All comments", "data": comment_data}, 200

    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error retrieving comments", "error": str(e)}, 500

def update_comment(current_user, comment_id, post_id, data):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Post not found"}, 404

    comment = Comment.query.filter_by(post_id=post_id, id=comment_id).first()
    if not comment:
        return {'status': "failed", "statusCode": 404, "message": "Comment not found"}, 404

    # Check if the user is an admin or the comment owner
    if current_user.role == 'admin' or current_user.id == comment.user_id:
        comment.comment = data['comment']
        db.session.commit()
        create_notification(post.owner_id, f"User {comment.user_id} updated comment on your post.")
        return {'status': "success", "statusCode": 200, "message": "Comment updated successfully"}, 200
    else:
        return {'status': "failed", "statusCode": 403, "message": "Permission denied; not an admin or the comment owner"}, 403


def delete_comment(current_user, comment_id, post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Post not found"}, 404

    comment = Comment.query.filter_by(post_id=post_id, id=comment_id).first()
    if not comment:
        return {'status': "failed", "statusCode": 404, "message": "Comment not found"}, 404

    # Check if the user is an admin or the comment owner
    if current_user.role == 'admin' or current_user.id == comment.user_id:
        db.session.delete(comment)
        db.session.commit()
        create_notification(post.owner_id, f"User {comment.user_id} deleted comment on your post.")
        return {'status': "success", "statusCode": 200, "message": "Comment deleted successfully"}, 200
    else:
        return {'status': "failed", "statusCode": 403, "message": "Permission denied; not an admin or the comment owner"}, 403


def create_like(user_id,post_id,data):
    user = User.query.filter_by(id=user_id).first()
    if not user :
        return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404
    
    user_id=user.id
    if not data:
        return {'status': "failed", "statusCode": 400, "message": "data required"}, 400  
    
    liked=data.get("liked") == 'true'
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return {'status': "failed", "statusCode": 404, "message": "No posts found"}, 404  # Handle no users case
    
    new_like = Post_Like(liked=liked,user_id=user_id, post_id=post.id)
    db.session.add(new_like)
    db.session.commit()
    create_notification(post.owner_id, f"User {user_id} liked  your post.")
    return {'status': "success", "statusCode": 201, "message": "like created successfully"}, 201

def update_like(current_user, like_id, post_id, data):
    # Check if the post exists
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Post not found"}, 404
    
    # Check if the like exists
    like = Post_Like.query.filter_by(post_id=post_id, id=like_id).first()
    if not like:
        return {'status': "failed", "statusCode": 404, "message": "Like not found"}, 404

    # Check permissions: user must be an admin or the owner of the like
    if current_user.role == 'admin' or current_user.id == like.user_id:
        like.liked = data.get("liked") == 'true'  # Convert to boolean
        db.session.commit()
        create_notification(post.owner_id, f"User {like.user_id} updated liked on your post.")
        return {'status': "success", "statusCode": 200, "message": "Like updated successfully"}, 200
    else:
        return {'status': "failed", "statusCode": 403, "message": "Permission denied"}, 403


def delete_like(current_user, like_id, post_id):
    # Check if the post exists
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Post not found"}, 404
    
    # Check if the like exists
    like = Post_Like.query.filter_by(post_id=post_id, id=like_id).first()
    if not like:
        return {'status': "failed", "statusCode": 404, "message": "Like not found"}, 404

    # Check permissions: user must be an admin or the owner of the like
    if current_user.role == 'admin' or current_user.id == like.user_id:
        db.session.delete(like)
        db.session.commit()
        create_notification(post.owner_id, f"User {like.user_id} updated commente on your post.")
        return {'status': "success", "statusCode": 200, "message": "Like deleted successfully"}, 200
    else:
        return {'status': "failed", "statusCode": 403, "message": "Permission denied"}, 403

#task 18 related work 

def follow_user(follower_id, followed_id):
    user= User.query.filter_by(id=followed_id).first()
    if user:
        # Check if the user is already following
        existing_follow = Follower.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if existing_follow:
            return {'status': "success", "statusCode": 200, "message": "Already following"}, 200
        
        # Create a new follow relationship
        new_follow = Follower(follower_id=follower_id, followed_id=followed_id)
        db.session.add(new_follow)
        db.session.commit()
        create_notification(followed_id, f"User {follower_id} started following you.")
        return {'status': "success", "statusCode": 200, "message": "Followed successfully"}, 200
    else:
         return {'status': "success", "statusCode": 200, "message": "No user exits to follow"}, 200


def unfollow_user(follower_id, followed_id):
    # Check if the follow relationship exists
    follow = Follower.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if not follow:
        return {'status': "success", "statusCode": 200, "message": "Not following"}, 200
    
    # Delete the follow relationship
    db.session.delete(follow)
    db.session.commit()
    create_notification(followed_id, f"User {follower_id} unfollowed you.")
    return {'status': "success", "statusCode": 200, "message": "Unfollowed successfully"}, 200

def notification_user(current_user):
    notifications = Notification.query.filter_by(user_id=current_user.id)
    if not notifications:
        return {'status': "success", "statusCode": 200, "message": "No notifications found for the user"}, 200
    
    notification_data = [notification.notification_to_dict() for notification in notifications]
    return {'status': "success", "statusCode": 200, "message": "All comments", "data": notification_data}, 200