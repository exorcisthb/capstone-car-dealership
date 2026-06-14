# Fullstack Developer Capstone

[![Django CI/CD](https://github.com/exorcisthb/xrwvm-fullstack_developer_capstone/actions/workflows/django-ci-cd.yml/badge.svg)](https://github.com/exorcisthb/xrwvm-fullstack_developer_capstone/actions/workflows/django-ci-cd.yml)

## Project Name
**Fullstack Developer Capstone**

## Project Description
A full-stack web application built as the **Fullstack Developer Capstone** project. The platform allows users to:
- Browse car dealerships across multiple US states
- Filter dealerships by state
- Read customer reviews for each dealership
- Sign up and post their own reviews
- Get automatic sentiment analysis (positive/negative/neutral) on reviews

## Tech Stack
- **Backend:** Python 3.11, Django 4.2
- **Frontend:** HTML5, CSS3, JavaScript, React
- **Database:** SQLite (development)
- **CI/CD:** GitHub Actions

## Local Setup

```bash
cd server
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Default Test Credentials
- **Root admin:** username `root`, password `rootpass123`
- **Test user:** username `testuser`, password `TestPass123`

## REST API Endpoints

| Method | Endpoint                                | Description                       |
|--------|-----------------------------------------|-----------------------------------|
| POST   | /djangoapp/login                        | Login (JSON: userName, password)  |
| GET    | /djangoapp/logout                       | Logout current user               |
| POST   | /djangoapp/register                     | Register new user                 |
| GET    | /djangoapp/dealers                      | List all dealers                  |
| GET    | /djangoapp/dealer/<id>                  | Get one dealer                    |
| GET    | /djangoapp/dealers/state/<state>        | Dealers in a state                |
| GET    | /djangoapp/reviews/dealer/<id>          | Reviews for a dealer              |
| POST   | /djangoapp/reviews/add                  | Add a review (login required)     |
| GET    | /djangoapp/carmakes                     | All car makes with models         |
| GET    | /djangoapp/get_cars                     | All car makes with models (CarModels) |
| GET    | /djangoapp/analyze/<text>               | Analyze sentiment of text         |
| GET    | /                                      | Home page (dealer list)           |

## License
This project is part of the Fullstack Developer Capstone course.
