# Social Network API Documentation

Welcome to the Social Network API! This project documentation is a Django REST API application for a social networking platform. It provides various functionalities such as user authentication, friend requests, and user search.

## Requirements

All the installed packages and their versions are listed in the requirements.txt file, which serves as a record of the project dependencies.

### Dependencies:


- Django==4.2.13
- django-ratelimit==4.1.0
- djangorestframework==3.15.1
- djangorestframework-simplejwt==5.3.1
- mysqlclient==2.2.4
- packaging==24.1
- PyJWT==2.8.0
- PyMySQL==1.1.1
- python-dotenv==1.0.1
- ratelimit==2.2.1

## Getting Started
Follow these steps to get the project up and running on your local machine.


1. Clone the Repository:

    ```bash
      git clone https://github.com/sangeeta-math/SocialNetworkProject.git

2. Navigate to the root directory of your Django project using the terminal or command prompt.

    ```bash
    cd social_network 

3. Create and Activate a Virtual Environment
   ```bash 
   python3 -m venv venv
   source venv/bin/activate

4. Install the dependencies from the requirements.txt file:

    ```bash
    pip install -r requirements.txt


5. *Database Configuration:*

   Open the settings.py file in your Django project and update the DATABASES setting with your MySQL database credentials.
    ```bash
   python DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'OPTIONS': {
               'init_command': "SET default_storage_engine=INNODB",
           },
           'NAME': 'database name',     # Replace with your database name
           'USER': 'your username',     # Replace with your MySQL server username
           'PASSWORD': 'your password', # Replace with your database password
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }


7. Apply migrations:

    ```bash
       python manage.py migrate
    

8. Run the server:

    ```bash 
        python manage.py runserver

## Using Docker
```bash 
    1. cd social_network
    2. chmod +x wait-for-db.sh
    3. docker-compose build
    4. docker-comppose up
    5. docker-compose exec web python manage.py migrate # This has to be done in a new terminal at the exact directory
```
#### Access the application at ```The http link given in the terminal``` in your web browser.

## Table of Contents

1. [Register User](#1-register-user)
2. [User Login](#2-user-login)
3. [User Logout](#3-user-logout)
4. [Search Users](#4-search-users)
5. [Send Friend Request](#5-send-friend-request)
6. [Accept Friend Request](#6-accept-friend-request)
7. [Reject Friend Request](#7-reject-friend-request)
8. [List Friends](#8-list-friends)
9. [List Pending Friends](#9-list-pending-friends)

## 1. Register User

- **URL**: `{{base-url}}api/users/`
- **Method**: `POST`
- **Body** (JSON):
  ```json
  {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "password123"
  }
  
- **Explanation**: This response indicates that a new user has been successfully created. It includes the user's ID, username, and email.

## 1. User Login

- **URL**: `{{base-url}}api/users/login/`
- **Method**: `POST`
- **Body** (JSON):
  ```json
  {
      "email": "newuser@example.com",
      "password": "password123"
  }

- **Explanation**: This response indicates successful authentication. It returns the username, an access token, and a refresh token.

## User Logout
- **URL**: `{{base-url}}api/users/logout/`
- **Method**: `POST`
- **Headers**:
  - Authorization: Bearer <access_token>
- **Body** (JSON):
  ```json
  {
    "refresh_token": "refresh_token_value"
  }

- **Explanation**: This response indicates that the user has been successfully logged out and the refresh token has been invalidated.

## Search Users
- **URL**: `{{base-url}}api/users/search/`
- **Method**: `GET`
- **Headers**:
  - Authorization: Bearer <access_token>
- **Query Params**:
  - search: search_term
- **Explanation**: This response returns a list of users matching the search term. Each user object includes the user's ID, username, first name, last name, and email.

## Send Friend Request
- **URL**:  `{{base-url}}api/users/friend-requests/`
- **Method**: `POST`
- **Headers**:
  - Authorization: Bearer <access_token>
- **Body (JSON)**:
  ```json
    {
        "to_user_id": 2
    }
- **Explanation**: This response indicates that the friend request was successfully sent.

## Accept Friend Request
- **URL**:  `{{base-url}}api/users/friend-requests/<request_id>/accept_request/`
- **Method**: `PUT`
- **Headers**:
  - Authorization: Bearer <access_token>
  
- **Explanation**: This response indicates that the friend request was successfully accepted.

 
## Reject Friend Request
- **URL**:  `{{base-url}}api/users/friend-requests/<request_id>/reject_request/`
- **Method**: `PUT`
- **Headers**:
  - Authorization: Bearer <access_token>
- **Explanation**: This response indicates that the friend request was successfully declined.



## List Friend
- **URL**:  `{{base-url}}api/users/friend-requests/list_friends/`
- **Method**: `GET`
- **Headers**:
  - Authorization: Bearer <access_token>
- **Explanation**: This response returns a list of friends. Each friend object includes the user's ID, username, first name, last name, and email.


## List Pending Friends
- **URL**:  `{{base-url}}api/users/friend-requests/list_pending_requests/`
- **Method**: `GET`
- **Headers**:
  - Authorization: Bearer <access_token>

- **Explanation**: This response returns a list of pending friend requests. Each pending friend object includes the user's ID, username, first name, last name, and email.

