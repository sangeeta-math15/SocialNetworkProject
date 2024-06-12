# Social Network API

This project is a Django REST API application for a social networking platform. It provides various functionalities such as user authentication, friend requests, and user search.

## Installation

### Clone the Repository

```bash
git clone https://github.com/sangeeta-math/SocialNetworkProject.git
```

### Navigate to the Project Directory
cd social_network

### Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate

### Install Dependencies
pip install -r requirements.txt


### Run Migrations
python manage.py migrate

### Start the Django Development Server
python manage.py runserver

#### Access the application at http://localhost:8000 in your web browser.

# Docker
### Build the Docker Image
docker-compose build

### Start the Docker Containers
docker-compose up

#### Access the application at http://localhost:8000 in your web browser.

# API Endpoints
### User Authentication
- POST /api/login/: Login with username and password.
- POST /api/register/: Register a new user.
### Friend Requests
- POST /api/users/friend-requests/: Send a friend request.
- PUT /api/users/friend-requests/{request_id}/accept/: Accept a friend request.
- PUT /api/users/friend-requests/{request_id}/reject/: Reject a friend request.
- GET /api/users/list_friends/: List of friends.
- GET /api/users/friend-requests/list_pending_requests/: List of pending friend requests.
### User Search
- GET /api/users/search/?search={search_term}: Search users by email or name.