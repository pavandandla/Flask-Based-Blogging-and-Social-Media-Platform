from config.database import db
from config.config import bcrypt
from datetime import datetime 


class User(db.Model):

    __tablename__ = 'User'  # Correct table name: 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    # One-to-many relationship with Post
    posts = db.relationship('Post', backref='owner', cascade='all, delete-orphan', lazy=True)
    followers = db.relationship('Follower', foreign_keys='Follower.followed_id', backref='followed', lazy=True)
    following = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower', lazy=True)
    notifications = db.relationship('Notification', foreign_keys='Notification.user_id', backref='notification', lazy=True)
    
    def user_to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'posts': [post.post_to_dict() for post in self.posts], # Serialize related posts
            'followers': len(self.followers),
            'following': len(self.following)
        }


class Post(db.Model):
    __tablename__ = 'Post'  # Correct table name: 'Post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # ForeignKey with cascade on delete for User
    owner_id = db.Column(
        db.Integer, 
        db.ForeignKey('User.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'User.id'
        nullable=False
    )

    # One-to-many relationship with Comment
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy=True)
    likes = db.relationship('Post_Like', backref='post', cascade='all, delete-orphan', lazy=True)

    def post_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'owner_id': self.owner_id,
            'comments': [comment.comment_to_dict() for comment in self.comments],  # Serialize related comments
            'likes': [like.like_to_dict() for like in self.likes],  # Serialize related comments
            'like_count': len(self.likes)
        }
    
class Follower(db.Model):
    __tablename__ = 'Follower'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id', ondelete='CASCADE'),
        nullable=False
    )
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id', ondelete='CASCADE'),
        nullable=False
    )

    def follower_to_dict(self):
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'followed_id': self.followed_id
            
        }


class Comment(db.Model):
    __tablename__ = 'Comment'  # Correct table name: 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    
    # ForeignKey with cascade on delete for User
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('User.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'User.id'
        nullable=False
    )
    
    # ForeignKey with cascade on delete for Post
    post_id = db.Column(
        db.Integer, 
        db.ForeignKey('Post.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'Post.id'
        nullable=False
    )
    
    def comment_to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'post_id': self.post_id,
            'user_id': self.user_id
        }
    
class Post_Like(db.Model):
    __tablename__ = 'Post_Like'

    id = db.Column(db.Integer, primary_key=True)
    liked = db.Column(db.Boolean, default=False)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('User.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'User.id'
        nullable=False
    )
    
    # ForeignKey with cascade on delete for Post
    post_id = db.Column(
        db.Integer, 
        db.ForeignKey('Post.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'Post.id'
        nullable=False
    )
    
    def like_to_dict(self):
        return {
            'id': self.id,
            'liked': self.liked,
        }

#completed=form_data.get("completed") == 'true',  # Convert to boolean

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def notification_to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
    
"""
 One-to-Many Relationship with Post
posts = db.relationship('Post', backref='owner', cascade='all, delete-orphan', lazy=True)
posts =:
Represents all the posts authored by a user.

db.relationship('Post', ...):
Establishes a one-to-many relationship between the User model and the Post model.

backref='owner':
Creates a bidirectional relationship where each Post object can access the associated User object using the owner attribute.

cascade='all, delete-orphan':
Ensures cascading behavior:

all: Any changes to a User object (like deletion) will cascade to their related posts.
delete-orphan: If a post loses its association with a user, it will be automatically deleted.
lazy=True:
Specifies lazy loading, meaning related posts will be loaded when accessed.

User ↔ Post (One-to-Many):
A user can create multiple posts.

User ↔ Follower (Self-referential Many-to-Many):
Users can follow/unfollow each other.

User ↔ Notification (One-to-Many):
Each user can have multiple notifications.

Post ↔ Comment (One-to-Many):
A post can have multiple comments.

Post ↔ Post_Like (One-to-Many):
A post can have multiple likes.

User ↔ Comment (Many-to-One):
A comment is linked to the user who authored it.

User ↔ Post_Like (Many-to-One):
A like is linked to the user who liked the post.
"""