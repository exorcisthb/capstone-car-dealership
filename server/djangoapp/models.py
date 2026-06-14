"""
Models for Car Dealership Review Platform.
Dealer, Review, CarMake, CarModel.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CarMake(models.Model):
    """Car make (brand), e.g. Toyota, BMW, Ford."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Car model belonging to a CarMake."""
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    COUPE = 'coupe'
    TRUCK = 'truck'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (HATCHBACK, 'Hatchback'),
        (COUPE, 'Coupe'),
        (TRUCK, 'Truck'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"


class Dealer(models.Model):
    """A car dealership."""
    STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]

    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    address = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    short_name = models.CharField(max_length=100, blank=True)
    logo_url = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"


class Review(models.Model):
    """Customer review for a dealer."""
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    review_text = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.SET_NULL, null=True, blank=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, default='neutral')  # positive/negative/neutral
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} review for {self.dealer.full_name}"
