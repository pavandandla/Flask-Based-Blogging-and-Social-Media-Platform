from flask import Blueprint
from controllers.user_controller import (
    signup,
    login,
    logout,
    create_post,
    get_post,
    create_comment,
    get_comment,
    update_post,
    delete_post,
    update_comment,
    delete_comment,
    create_like,
    update_like,
    delete_like,
    follow,
    unfollow,
    notification
    
)

# Blueprint for user authentication routes
user_bp = Blueprint('user_bp', __name__)

# Define routes
user_bp.route('/signup', methods=['POST'])(signup)
user_bp.route('/login', methods=['POST'])(login)
user_bp.route('/logout', methods=['POST'])(logout)
user_bp.route('/create-post', methods=['POST'])(create_post)
user_bp.route('/get-post/', methods=['GET'])(get_post)
user_bp.route('/update-post/<int:post_id>', methods=['PUT'])(update_post)
user_bp.route('/delete-post/<int:post_id>', methods=['DELETE'])(delete_post)
user_bp.route('/create-comment', methods=['POST'])(create_comment)
user_bp.route('/get-comment/<int:post_id>', methods=['GET'])(get_comment)
user_bp.route('/update-comment/<int:comment_id>', methods=['PUT'])(update_comment)
user_bp.route('/delete-comment/<int:comment_id>', methods=['DELETE'])(delete_comment)
user_bp.route('/create-like', methods=['POST'])(create_like)
user_bp.route('/update-like/<int:like_id>', methods=['PUT'])(update_like)
user_bp.route('/delete-like/<int:like_id>', methods=['DELETE'])(delete_like)
user_bp.route('/follow/<int:target_id>', methods=['POST'])(follow)
user_bp.route('/unfollow/<int:target_id>', methods=['POST'])(unfollow)
user_bp.route('/notification', methods=['POST'])(notification)
