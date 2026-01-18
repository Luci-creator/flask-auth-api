# Flask Auth API

A simple user authentication API built with Flask, JWT, and Flask-Limiter.  
Supports user registration, login, profile management, account updates, and account deactivation with rate limiting.

## Features

- User registration with password hashing
- Login with JWT authentication
- Protected routes for user profile
- Update password
- Deactivate account
- Rate limiting to prevent brute-force attacks

## Technologies

- Python 3
- Flask
- Flask-JWT-Extended
- Flask-Limiter
- Flask-SQLAlchemy
- Werkzeug (for password hashing)

## Installation

1. Clone the repo:

```bash
git clone https://github.com/Luci-creator/flask-auth-api.git
cd flask-auth-api
