# Deployment Guide (Tasks 24-28)

This guide explains how to deploy the Django app for Tasks 24-28.

## Option 1: Render.com (recommended, free tier)

1. Push this repository to GitHub (you must have done this for Task 1 already).
2. Go to https://render.com and sign in.
3. Click **New +** → **Web Service**.
4. Connect your GitHub repo.
5. Configure:
   - **Root Directory:** `server`
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn djangoproject.wsgi --log-file -`
   - **Instance Type:** Free
6. Click **Create Web Service**.
7. Wait for the deploy to finish; copy the public URL (e.g. `https://capstone-cardealer.onrender.com`).
8. After deploy, open a shell in Render and run:
   ```bash
   python manage.py seed_data
   python manage.py createsuperuser   # optional
   ```
9. Save the URL in `deploymentURL.txt`.
10. On your local machine, capture the deployment screenshots:
    ```powershell
    $env:DEPLOY_URL = "https://capstone-cardealer.onrender.com"
    python capture_deployment_screenshots.py
    ```
    This will create:
    - `deployed_landingpage.png`  (Task 25)
    - `deployed_loggedin.png`     (Task 26)
    - `deployed_dealer_detail.png`(Task 27)
    - `deployed_add_review.png`   (Task 28)

## Option 2: Railway.app (free tier)

1. Push to GitHub.
2. Go to https://railway.app → **New Project** → **Deploy from GitHub Repo**.
3. Set **Root Directory** to `server`.
4. Railway auto-detects the `Procfile` and `runtime.txt`.
5. After deploy, run in the Railway shell:
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```
6. Click **Generate Domain** to get a public URL.
7. Save the URL in `deploymentURL.txt` and capture screenshots (see step 10 above).

## Option 3: Heroku

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. ```bash
   heroku login
   heroku create capstone-cardealer
   heroku config:set DJANGO_SETTINGS_MODULE=djangoproject.settings
   git subtree push --prefix server heroku main
   heroku run python manage.py migrate
   heroku run python manage.py seed_data
   ```
3. Visit `https://capstone-cardealer.herokuapp.com` to confirm.

## Required Files (already in this repo)

- `server/Procfile` - process declaration for gunicorn
- `server/runtime.txt` - Python version pin
- `server/requirements.txt` - dependencies
- `server/djangoproject/settings.py` - configured with `ALLOWED_HOSTS = ['*']` and `whitenoise` for static files

## Notes

- The default database is SQLite (great for free deploys). For production, switch to PostgreSQL.
- Static files are served by `whitenoise`, so no extra CDN needed.
- For the screenshots to display the user is logged in, you must first run `seed_data` so the `testuser` account exists.
