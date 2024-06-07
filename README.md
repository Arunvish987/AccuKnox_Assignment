# Django Friend Request API

This project provides APIs for user authentication, searching users, and managing friend requests (sending, accepting, rejecting, and listing friends).

## Features

- User Authentication (Login)
- Search Users by Email or Name
- Send Friend Requests with Rate Limiting
- Accept and Reject Friend Requests
- List Friends
- List Pending Friend Requests

## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.7 or higher
- Django 3.0 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository:**
   
   git clone https://github.com/Arunvish987/AccuKnox_Assignment.git
   cd your-repo-name

2. Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Create and run migrations:

   python manage.py makemigrations
   python manage.py migrate

4. Run the development server:

   python manage.py runserver

5. Access the project:

    API Documentation: Visit http://127.0.0.1:8000/
    Admin Panel: Visit http://127.0.0.1:8000/admin


######**********************############***************###################************************############

API Endpoints
User Authentication

1. Login
    POST /login/

Request:
{
    "email": "user@example.com",
    "password": "password"
}

Response:
{
    "refresh": "token",
    "access": "token"
}

2. Search Users
   GET /search/?query=<search_term>&page=<page_number>

Request:
    POST /friend-request/send/

    {
    "sender_id": 1,
    "receiver_id": 2
    }

3. Accept Friend Request:
   POST /friend-request/accept/

Request:
    {
    "request_id": 1
    }

4. Reject Friend Request:
   POST /friend-request/reject/

Request:
    {
    "request_id": 1
    }

5. List Friends:
   GET /list_pending_requests/?user_id=int

Request:
    user_id 

6. List Pending Friend Requests:
   GET /friend-request/?user_id=int

Request:
    user_id




### Explanation:
- **Installation Steps**: Provides a step-by-step guide to setting up the project locally, including cloning the repository, creating a virtual environment, installing dependencies, creating and running migrations, and starting the development server.
- **API Endpoints**: Lists the available API endpoints with their respective request formats and examples.
- **Additional Notes**: Mentions additional configuration steps and adjustments.
- **License**: Includes a placeholder for the project's license.

This `README.md` file should provide clear instructions for setting up and using the project, along with details about the available API endpoints. Adjust the URLs and repository details as needed to match your actual project setup.


    





    


   



