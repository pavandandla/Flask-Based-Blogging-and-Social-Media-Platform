from flask import Blueprint
from controllers.user_controller import (
    signup, 
    login, 
    get_userdata, 
    update_post,
    delete_post,
    update_comment,
    delete_comment,
    get_post,
    create_like,
    update_like,
    delete_like
)
# Blueprint for user authentication routes
admin_bp = Blueprint('admin_bp', __name__)

# Define routes
admin_bp.route('/signup', methods=['POST'])(signup)
admin_bp.route('/login', methods=['POST'])(login)
admin_bp.route('/get-userdata', methods=['GET'])(get_userdata)
admin_bp.route('/get-post/', methods=['GET'])(get_post)
admin_bp.route('/update-post/<int:post_id>', methods=['PUT'])(update_post)
admin_bp.route('/delete-post/<int:post_id>', methods=['DELETE'])(delete_post)
admin_bp.route('/update-comment/<int:comment_id>', methods=['PUT'])(update_comment)
admin_bp.route('/delete-comment/<int:comment_id>', methods=['DELETE'])(delete_comment)
admin_bp.route('/create-like', methods=['POST'])(create_like)
admin_bp.route('/update-like/<int:like_id>', methods=['PUT'])(update_like)
admin_bp.route('/delete-like/<int:like_id>', methods=['DELETE'])(delete_like)

