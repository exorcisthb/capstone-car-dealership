"""
URL configuration for the djangoapp (REST API + page routes).
"""
from django.urls import path
from . import views

urlpatterns = [
    # Page routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dealer/<int:dealer_id>/', views.dealer_detail, name='dealer_detail'),

    # Auth
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register_user, name='register_user'),

    # Dealer APIs
    path('dealers', views.get_dealers, name='get_dealers'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('dealers/state/<str:state>', views.get_dealers_by_state, name='get_dealers_by_state'),

    # Review APIs
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('reviews/add', views.add_review, name='add_review'),

    # Car make API
    path('carmakes', views.get_all_car_makes, name='get_all_car_makes'),

    # Sentiment
    path('analyze', views.analyze_review, name='analyze_review'),
]
