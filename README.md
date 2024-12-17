# **Flask-Based Blogging and Social Media Platform**

## **Description**

This project is a **Blogging and Social Media Platform** built with **Flask** and **MySQL**. Users can register, log in, create, edit, delete, and view blog posts. The platform includes features like a news feed, notifications, comments, and likes. Additionally, users can follow others, interact with posts, and build a social presence.



## **Features**

- **Secure Authentication and Authorization**  
    Implements user registration, login, and session management with secure authentication using **JWT**.
    
- **Efficient Database Operations**  
    Optimized database operations using **Flask-SQLAlchemy** with **MySQL** for efficient storage and retrieval of user data, posts, comments, likes, and follower relationships.
    
- **Email Functionality**  
    Sends email notifications for events like post updates, comments, and follows.
    
- **Environment Configuration**  
    Uses environment variables for configuration management, making it easy to set up in different environments.
    
- **Modular Code Organization**  
    Follows a modular structure for maintainability and scalability, separating models, controllers, services, and routes.
    
- **Standardized API Responses**  
    Ensures consistent and clear API responses for seamless communication between the client and server.
    
- **News Feed and Follower/Following Relationship**  
    Users can see a personalized news feed based on the users they follow, along with a system for following and unfollowing others.
    
- **Comprehensive Error Handling**  
    Implements error handling throughout the application to ensure a smooth user experience.
    


## Prerequisites

- Python 3.9+
- pip
- Virtual environment support

## **Libraries Used**

- **Flask** 
- **Flask-SQLAlchemy**
- **MySQL** 
- **Flask-Mail** 
- **JWT** 
- **Python-dotenv** 

## **Installation and Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/pavandandla/Flask-Based-Blogging-and-Social-Media-Platform.git
cd Flask-Based-Blogging-and-Social-Media-Platform
```



### **2. Create a Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```



### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```



### **4. Configure Environment Variables**

Create a `.env` file in the root directory with the following configuration:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=mysql://username:password@localhost/db_name
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password
FLASK_ENV=development
```

- **SECRET_KEY**: A key for securely signing JWT tokens.
- **DATABASE_URL**: MySQL connection string.
- **EMAIL_HOST**: SMTP server for email functionality.
- **EMAIL_PORT**: Port for SMTP server.
- **EMAIL_USER**: Your email address for sending notifications.
- **EMAIL_PASSWORD**: Your email password.
- **FLASK_ENV**: Set to `development` for debugging.



### **5. Set Up the Database**

Run the following command to initialize the database and create necessary tables:

```bash
python src/init_db.py
```



### **6. Run the Application**

To run the Flask application, execute:

```bash
flask run
```

The application will be available at: `http://127.0.0.1:5000`





## **Example Workflow**

1. **User Registration and Authentication**  
    Users can register and log in using the `/register` and `/login` endpoints. Upon successful login, they receive a JWT token for authentication.
    
2. **Create and Manage Posts**  
    Users can create, update, and delete blog posts via the `/posts` endpoint. Each post can have multiple comments and likes.
    
3. **Interacting with Posts**  
    Users can like posts and comment on them. Comments can be created using the `/comments` endpoint, and posts can be liked using the `/like` endpoint.
    
4. **Follower/Following Relationships**  
    Users can follow and unfollow other users, influencing their personalized news feed which displays updates from the users they follow.
    
5. **News Feed**  
    A personalized news feed is available for users to view posts from the users they follow.
    
6. **Email Notifications**  
    Users will receive email notifications for actions such as new comments, post updates, and follow/unfollow events.
    



## **Environment Configuration**

Example `.env` file:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=mysql://username:password@localhost/db_name
```


## **Contact**

For questions, suggestions, or issues, contact:

- GitHub: [pavandandla](https://github.com/pavandandla)
