"""
Seed the database with sample dealers, car makes, models, and reviews.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djangoapp.models import Dealer, CarMake, CarModel, Review
from djangoapp.sentiment import analyze_sentiment


DEALERS = [
    {
        'full_name': 'Best Cars of Kansas City',
        'short_name': 'Best Cars KC',
        'city': 'Kansas City', 'state': 'KS', 'zip_code': '66101',
        'address': '123 Main St', 'phone': '555-0101', 'email': 'sales@bestcarskc.com',
        'logo_url': 'https://images.unsplash.com/photo-1562519819-016930ada31b?w=400',
    },
    {
        'full_name': 'Topeka Auto Mall',
        'short_name': 'Topeka Auto',
        'city': 'Topeka', 'state': 'KS', 'zip_code': '66601',
        'address': '456 Kansas Ave', 'phone': '555-0102', 'email': 'sales@topekaauto.com',
        'logo_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400',
    },
    {
        'full_name': 'Wichita Premier Motors',
        'short_name': 'Wichita Premier',
        'city': 'Wichita', 'state': 'KS', 'zip_code': '67201',
        'address': '789 Douglas Ave', 'phone': '555-0103', 'email': 'sales@wichitapremier.com',
        'logo_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400',
    },
    {
        'full_name': 'Los Angeles Auto Gallery',
        'short_name': 'LA Auto',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001',
        'address': '100 Hollywood Blvd', 'phone': '555-0201', 'email': 'sales@laauto.com',
        'logo_url': 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=400',
    },
    {
        'full_name': 'New York Motors',
        'short_name': 'NY Motors',
        'city': 'New York', 'state': 'NY', 'zip_code': '10001',
        'address': '5th Avenue', 'phone': '555-0301', 'email': 'sales@nymotors.com',
        'logo_url': 'https://images.unsplash.com/photo-1542362567-b07e54358753?w=400',
    },
    {
        'full_name': 'Texas Lone Star Cars',
        'short_name': 'Lone Star',
        'city': 'Houston', 'state': 'TX', 'zip_code': '77001',
        'address': '50 Bayou Dr', 'phone': '555-0401', 'email': 'sales@lonestarcars.com',
        'logo_url': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=400',
    },
]

CAR_MAKES = [
    ('Toyota', 'Reliable Japanese automaker', [
        ('Camry', 'sedan', 2024), ('Corolla', 'sedan', 2024), ('RAV4', 'suv', 2024),
    ]),
    ('Honda', 'Quality and efficiency', [
        ('Civic', 'sedan', 2024), ('Accord', 'sedan', 2024), ('CR-V', 'suv', 2024),
    ]),
    ('Ford', 'American muscle and trucks', [
        ('F-150', 'truck', 2024), ('Mustang', 'coupe', 2024), ('Explorer', 'suv', 2024),
    ]),
    ('BMW', 'Luxury German engineering', [
        ('3 Series', 'sedan', 2024), ('X5', 'suv', 2024), ('M4', 'coupe', 2024),
    ]),
    ('Tesla', 'Electric vehicles', [
        ('Model 3', 'sedan', 2024), ('Model Y', 'suv', 2024), ('Model S', 'sedan', 2024),
    ]),
    ('Chevrolet', 'American classics', [
        ('Silverado', 'truck', 2024), ('Malibu', 'sedan', 2024), ('Equinox', 'suv', 2024),
    ]),
]

SAMPLE_REVIEWS = [
    ('John Smith', 'Fantastic services! The team was friendly and professional.', True, 2023),
    ('Mary Johnson', 'Terrible experience. They were rude and the car broke down.', False, None),
    ('David Lee', 'Great selection of cars and fair prices. Highly recommend!', True, 2022),
    ('Sarah Brown', 'The dealership was clean and the staff was helpful. Smooth process.', True, 2023),
    ('Mike Wilson', 'Average experience, nothing special but not bad either.', False, None),
    ('Emily Davis', 'Best car buying experience ever! Love my new car!', True, 2024),
    ('Robert Taylor', 'Slow service and the paperwork was a nightmare. Disappointing.', False, None),
    ('Lisa Anderson', 'Wonderful people, awesome deals. I am so happy with my purchase.', True, 2023),
]


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        # ----- Dealers -----
        for d in DEALERS:
            Dealer.objects.update_or_create(full_name=d['full_name'], defaults=d)
        self.stdout.write(self.style.SUCCESS(f'Created/updated {len(DEALERS)} dealers'))

        # ----- Car makes & models -----
        for make_name, make_desc, models in CAR_MAKES:
            make, _ = CarMake.objects.update_or_create(name=make_name, defaults={'description': make_desc})
            for mname, mtype, myear in models:
                CarModel.objects.update_or_create(
                    car_make=make, name=mname,
                    defaults={'type': mtype, 'year': myear},
                )
        self.stdout.write(self.style.SUCCESS(f'Created/updated {len(CAR_MAKES)} car makes'))

        # ----- Root user -----
        if not User.objects.filter(username='root').exists():
            User.objects.create_superuser('root', 'root@capstone.com', 'rootpass123')
            self.stdout.write(self.style.SUCCESS('Created root superuser (root/rootpass123)'))
        else:
            self.stdout.write('Root superuser already exists')

        # ----- Sample user (for login cURL) -----
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@example.com', 'TestPass123')
            self.stdout.write(self.style.SUCCESS('Created test user (testuser/TestPass123)'))

        # ----- Reviews -----
        dealers = list(Dealer.objects.all())
        makes = list(CarMake.objects.prefetch_related('car_models').all())
        for i, (name, text, purchased, year) in enumerate(SAMPLE_REVIEWS):
            dealer = dealers[i % len(dealers)]
            make = makes[i % len(makes)]
            model = list(make.car_models.all())[0]
            sentiment, _ = analyze_sentiment(text)
            Review.objects.create(
                dealer=dealer, name=name, review_text=text,
                purchase=purchased, car_year=year,
                car_make=make, car_model=model, sentiment=sentiment,
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(SAMPLE_REVIEWS)} reviews'))

        self.stdout.write(self.style.SUCCESS('=== Seed complete ==='))
