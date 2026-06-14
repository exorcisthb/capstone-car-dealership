"""
Views for Car Dealership Review Platform.

Includes:
- Home / About / Contact pages
- Authentication (login_user, logout_user, register)
- Dealer APIs (list, by id, by state)
- Review APIs (list by dealer, add, analyze sentiment)
- Car make/model APIs
"""
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Dealer, Review, CarMake, CarModel
from .sentiment import analyze_sentiment


# ============================================================
# Page Views (Home / About / Contact)
# ============================================================

def home(request):
    """Home page - list of dealers (with optional state filter)."""
    state = request.GET.get('state', '').upper()
    if state:
        dealers = Dealer.objects.filter(state=state)
    else:
        dealers = Dealer.objects.all()
    context = {
        'dealers': dealers,
        'state': state,
        'states': Dealer.STATE_CHOICES,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'About.html')


def contact(request):
    return render(request, 'Contact.html')


def dealer_detail(request, dealer_id):
    """Single dealer page with reviews and Post Review form."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return render(request, '404.html', status=404)
    reviews = dealer.reviews.all()
    car_makes = CarMake.objects.all()
    context = {
        'dealer': dealer,
        'reviews': reviews,
        'car_makes': car_makes,
    }
    return render(request, 'dealer_detail.html', context)


# ============================================================
# Authentication APIs
# ============================================================

@csrf_exempt
def login_user(request):
    """POST /djangoapp/login - login with username & password."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    username = data.get('userName') or data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'status': True,
            'userName': username,
            'message': 'Login successful'
        })
    return JsonResponse({
        'status': False,
        'userName': username,
        'message': 'Invalid username or password'
    }, status=401)


@csrf_exempt
def logout_user(request):
    """POST /djangoapp/logout - logout current user."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        return JsonResponse({
            'status': True,
            'userName': username,
            'message': f'User {username} logged out successfully'
        })
    return JsonResponse({
        'status': False,
        'message': 'No user is currently logged in'
    })


@csrf_exempt
def register_user(request):
    """POST /djangoapp/register - create a new user."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    username = data.get('userName') or data.get('username')
    password = data.get('password')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    if not username or not password:
        return JsonResponse({'error': 'username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    user = User.objects.create_user(
        username=username, password=password,
        first_name=first_name, last_name=last_name, email=email
    )
    login(request, user)
    return JsonResponse({
        'status': True,
        'userName': username,
        'message': 'Registration successful'
    })


# ============================================================
# Dealer REST APIs
# ============================================================

def get_dealers(request):
    """GET /djangoapp/dealers - list all dealers. Supports ?state=KS"""
    state = request.GET.get('state', '').upper()
    if state:
        dealers = Dealer.objects.filter(state=state)
    else:
        dealers = Dealer.objects.all()
    return JsonResponse({
        'status': True,
        'dealers': [serialize_dealer(d) for d in dealers]
    })


def get_dealer_by_id(request, dealer_id):
    """GET /djangoapp/dealer/<id> - single dealer details."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({'status': False, 'error': 'Dealer not found'}, status=404)
    return JsonResponse({'status': True, 'dealer': serialize_dealer(dealer)})


def get_dealers_by_state(request, state):
    """GET /djangoapp/dealers/state/<state> - dealers in a state."""
    state = state.upper()
    dealers = Dealer.objects.filter(state=state)
    if not dealers.exists():
        return JsonResponse({'status': False, 'error': f'No dealers found in {state}'}, status=404)
    return JsonResponse({'status': True, 'dealers': [serialize_dealer(d) for d in dealers]})


def serialize_dealer(d):
    return {
        'id': d.id,
        'full_name': d.full_name,
        'short_name': d.short_name or d.full_name,
        'city': d.city,
        'state': d.state,
        'address': d.address,
        'zip': d.zip_code,
        'phone': d.phone,
        'email': d.email,
        'logo_url': d.logo_url,
        'website': d.website,
    }


# ============================================================
# Review APIs
# ============================================================

def get_dealer_reviews(request, dealer_id):
    """GET /djangoapp/reviews/dealer/<dealer_id> - all reviews for a dealer."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({'status': False, 'error': 'Dealer not found'}, status=404)
    reviews = dealer.reviews.all()
    return JsonResponse({
        'status': True,
        'dealer_id': dealer_id,
        'reviews': [serialize_review(r) for r in reviews]
    })


@csrf_exempt
@login_required
def add_review(request):
    """POST /djangoapp/reviews/add - create a new review."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    try:
        dealer = Dealer.objects.get(id=data.get('dealer_id'))
    except Dealer.DoesNotExist:
        return JsonResponse({'error': 'Dealer not found'}, status=404)
    review_text = data.get('review', '')
    sentiment, score = analyze_sentiment(review_text)
    review = Review.objects.create(
        dealer=dealer,
        name=request.user.username,
        review_text=review_text,
        purchase=data.get('purchase', False),
        car_year=data.get('car_year'),
        sentiment=sentiment,
    )
    return JsonResponse({
        'status': True,
        'review': serialize_review(review),
        'sentiment': sentiment,
        'score': score,
    })


def serialize_review(r):
    return {
        'id': r.id,
        'dealer_id': r.dealer_id,
        'name': r.name,
        'review': r.review_text,
        'purchase': r.purchase,
        'purchase_date': r.purchase_date.isoformat() if r.purchase_date else None,
        'car_make': r.car_make.name if r.car_make else None,
        'car_model': r.car_model.name if r.car_model else None,
        'car_year': r.car_year,
        'sentiment': r.sentiment,
        'created_at': r.created_at.isoformat(),
    }


# ============================================================
# Car Make / Model APIs
# ============================================================

def get_all_car_makes(request):
    """GET /djangoapp/carmakes - all makes with their models."""
    makes = CarMake.objects.prefetch_related('car_models').all()
    data = []
    for m in makes:
        data.append({
            'id': m.id,
            'name': m.name,
            'description': m.description,
            'models': [
                {
                    'id': cm.id,
                    'name': cm.name,
                    'type': cm.type,
                    'year': cm.year,
                } for cm in m.car_models.all()
            ],
        })
    return JsonResponse({'status': True, 'car_makes': data})


# ============================================================
# Sentiment Analysis
# ============================================================

@csrf_exempt
def analyze_review(request):
    """POST /djangoapp/analyze - analyze sentiment of a review text."""
    if request.method == 'GET':
        text = request.GET.get('text', '')
    else:
        try:
            data = json.loads(request.body) if request.body else {}
            text = data.get('text', '')
        except json.JSONDecodeError:
            text = ''
    if not text:
        return JsonResponse({'status': False, 'error': 'text is required'}, status=400)
    sentiment, score = analyze_sentiment(text)
    return JsonResponse({
        'status': True,
        'text': text,
        'sentiment': sentiment,
        'score': score,
    })
