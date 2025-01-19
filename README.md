# Chatbot with WebSocket Concept and Role-Based Authentication

## Project Overview
This project is a chatbot application featuring:
- Real-time communication through WebSocket integration.
- Role-based authentication for users and admins.
- Asynchronous task processing using Celery.

The application demonstrates the integration of robust system design for real-time interaction and access control.

---

## Key Features

### 1. WebSocket Integration
- **Purpose**: Enables real-time communication between the client and server for seamless user interaction.
- **Implementation**: Uses WebSocket protocols (e.g., Django Channels) to manage real-time messaging between users and the chatbot.

### 2. User Authentication
- **Purpose**: Provides secure access to the application, enabling user login and interaction.
- **Features**:
  - User registration and login.
  - Role-based authentication with the following roles:
    - **User**: General role for interacting with the chatbot.
    - **Admin**: Role with additional privileges such as monitoring chat logs, configuring chatbot responses, and managing users.
  - Password hashing and secure  CSRF token-based authentication.


### 3. Role-Based Access Control
- **Purpose**: Restricts access to functionalities based on user roles.
- **Implementation**:
  - Two roles: **User** and **Admin**.
    - **Admin** has more permissions compared to **User**.
  - Decorators used:
    - `@login_required`: Ensures the user is authenticated.
    - `@user_passes_test`: Differentiates between admin and general users.

### 4. Celery for Asynchronous Tasks
- **Purpose**: Offloads time-consuming operations like:
  - Sending email notifications for user registration or password resets.
- **Implementation**: Utilizes Celery with a message broker like Redis to handle task queuing.
- **Example**: Automatically sends an email when a new user registers.

---

## Technologies Used
- **Backend**: Django, Django Channels
- **Frontend**: HTML,CSS,JS
- **Authentication**: Django Authentication, JWT
- **WebSocket**: Django Channels
- **Asynchronous Task Processing**: Celery with Redis
- **Database**: Sqllite3

---

## Installation and Setup

### Prerequisites
1. Python 3.8+
2. Redis for Celery
3. Sqllite3 database

### Steps
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd chatbot_websocket_auth
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Apply database migrations:
    ```bash
    python manage.py migrate
    python manage.py makemigrations <app name>
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Start Celery workers:
    ```bash
    celery -A chatapp worker -l info -P eventlet
    ```

6. Run the Redis server on port 6379.

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

---

## Usage
- **Users** can:
  - Register, log in, and chat with the bot.
  - Reset passwords through email notifications.

- **Admins** can:
  - Monitor chat logs.
  - Manage user accounts.
  - Configure chatbot responses.



## Future Enhancements
- Add support for multilingual chatbot responses.
- Implement AI-powered chatbot responses using NLP libraries (e.g., spaCy, TensorFlow).
- Enable detailed analytics for admin users.
- Add functionalities like:
  - Speech-to-text.
  - Auto text suggestions.
- Use React.js for an attractive and responsive frontend.
- Add notifications for important events or updates.
- Also make Custom Deshboard for Admin
- Create .env files and more secure project

---

## License
This project is licensed under the [MIT License](LICENSE).
