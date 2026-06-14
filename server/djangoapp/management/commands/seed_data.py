"""
Seed the database with 50 sample dealers (with lat/long), car makes, models, and reviews.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djangoapp.models import Dealer, CarMake, CarModel, Review
from djangoapp.sentiment import analyze_sentiment


# 50 US dealers (across multiple states), each with realistic latitude/longitude.
DEALERS = [
    # Kansas (3)
    {'full_name': 'Best Cars of Kansas City', 'short_name': 'Best Cars KC', 'city': 'Kansas City', 'state': 'KS', 'zip_code': '66101', 'address': '123 Main St', 'phone': '555-0101', 'email': 'sales@bestcarskc.com', 'latitude': 39.1141, 'longitude': -94.6275},
    {'full_name': 'Topeka Auto Mall', 'short_name': 'Topeka Auto', 'city': 'Topeka', 'state': 'KS', 'zip_code': '66601', 'address': '456 Kansas Ave', 'phone': '555-0102', 'email': 'sales@topekaauto.com', 'latitude': 39.0473, 'longitude': -95.6752},
    {'full_name': 'Wichita Premier Motors', 'short_name': 'Wichita Premier', 'city': 'Wichita', 'state': 'KS', 'zip_code': '67201', 'address': '789 Douglas Ave', 'phone': '555-0103', 'email': 'sales@wichitapremier.com', 'latitude': 37.6872, 'longitude': -97.3301},
    # California (5)
    {'full_name': 'Los Angeles Auto Gallery', 'short_name': 'LA Auto', 'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001', 'address': '100 Hollywood Blvd', 'phone': '555-0201', 'email': 'sales@laauto.com', 'latitude': 34.0522, 'longitude': -118.2437},
    {'full_name': 'San Francisco Bay Motors', 'short_name': 'SF Bay Motors', 'city': 'San Francisco', 'state': 'CA', 'zip_code': '94101', 'address': '500 Market St', 'phone': '555-0202', 'email': 'sales@sfbaymotors.com', 'latitude': 37.7749, 'longitude': -122.4194},
    {'full_name': 'San Diego Auto Center', 'short_name': 'SD Auto', 'city': 'San Diego', 'state': 'CA', 'zip_code': '92101', 'address': '200 Broadway', 'phone': '555-0203', 'email': 'sales@sdauto.com', 'latitude': 32.7157, 'longitude': -117.1611},
    {'full_name': 'Sacramento Valley Cars', 'short_name': 'Sac Valley', 'city': 'Sacramento', 'state': 'CA', 'zip_code': '95814', 'address': '120 Capitol Mall', 'phone': '555-0204', 'email': 'sales@sacvalley.com', 'latitude': 38.5816, 'longitude': -121.4944},
    {'full_name': 'San Jose Auto Plaza', 'short_name': 'SJ Auto', 'city': 'San Jose', 'state': 'CA', 'zip_code': '95110', 'address': '88 First St', 'phone': '555-0205', 'email': 'sales@sjauto.com', 'latitude': 37.3382, 'longitude': -121.8863},
    # New York (4)
    {'full_name': 'New York Motors', 'short_name': 'NY Motors', 'city': 'New York', 'state': 'NY', 'zip_code': '10001', 'address': '5th Avenue', 'phone': '555-0301', 'email': 'sales@nymotors.com', 'latitude': 40.7128, 'longitude': -74.0060},
    {'full_name': 'Brooklyn Auto House', 'short_name': 'Brooklyn Auto', 'city': 'Brooklyn', 'state': 'NY', 'zip_code': '11201', 'address': '300 Atlantic Ave', 'phone': '555-0302', 'email': 'sales@brooklynauto.com', 'latitude': 40.6782, 'longitude': -73.9442},
    {'full_name': 'Buffalo Great Lakes Cars', 'short_name': 'Buffalo GL', 'city': 'Buffalo', 'state': 'NY', 'zip_code': '14202', 'address': '45 Main St', 'phone': '555-0303', 'email': 'sales@buffalogl.com', 'latitude': 42.8864, 'longitude': -78.8784},
    {'full_name': 'Albany Empire Motors', 'short_name': 'Albany Empire', 'city': 'Albany', 'state': 'NY', 'zip_code': '12207', 'address': '12 State St', 'phone': '555-0304', 'email': 'sales@albanyempire.com', 'latitude': 42.6526, 'longitude': -73.7562},
    # Texas (5)
    {'full_name': 'Texas Lone Star Cars', 'short_name': 'Lone Star', 'city': 'Houston', 'state': 'TX', 'zip_code': '77001', 'address': '50 Bayou Dr', 'phone': '555-0401', 'email': 'sales@lonestarcars.com', 'latitude': 29.7604, 'longitude': -95.3698},
    {'full_name': 'Dallas Big D Motors', 'short_name': 'Big D', 'city': 'Dallas', 'state': 'TX', 'zip_code': '75201', 'address': '200 Elm St', 'phone': '555-0402', 'email': 'sales@bigdmotors.com', 'latitude': 32.7767, 'longitude': -96.7970},
    {'full_name': 'Austin Live Oak Auto', 'short_name': 'Live Oak', 'city': 'Austin', 'state': 'TX', 'zip_code': '78701', 'address': '110 Congress Ave', 'phone': '555-0403', 'email': 'sales@liveoak.com', 'latitude': 30.2672, 'longitude': -97.7431},
    {'full_name': 'San Antonio Riverwalk Cars', 'short_name': 'Riverwalk', 'city': 'San Antonio', 'state': 'TX', 'zip_code': '78205', 'address': '400 Commerce St', 'phone': '555-0404', 'email': 'sales@riverwalk.com', 'latitude': 29.4241, 'longitude': -98.4936},
    {'full_name': 'Fort Worth Stockyard Motors', 'short_name': 'Stockyard', 'city': 'Fort Worth', 'state': 'TX', 'zip_code': '76102', 'address': '131 E Exchange Ave', 'phone': '555-0405', 'email': 'sales@stockyard.com', 'latitude': 32.7555, 'longitude': -97.3308},
    # Florida (4)
    {'full_name': 'Miami Sun Motors', 'short_name': 'Sun Motors', 'city': 'Miami', 'state': 'FL', 'zip_code': '33101', 'address': '100 Biscayne Blvd', 'phone': '555-0501', 'email': 'sales@sunmotors.com', 'latitude': 25.7617, 'longitude': -80.1918},
    {'full_name': 'Orlando Theme Park Cars', 'short_name': 'Theme Park', 'city': 'Orlando', 'state': 'FL', 'zip_code': '32801', 'address': '50 Orange Ave', 'phone': '555-0502', 'email': 'sales@themepark.com', 'latitude': 28.5383, 'longitude': -81.3792},
    {'full_name': 'Tampa Bay Auto Center', 'short_name': 'Tampa Bay', 'city': 'Tampa', 'state': 'FL', 'zip_code': '33602', 'address': '400 Ashley Dr', 'phone': '555-0503', 'email': 'sales@tampabay.com', 'latitude': 27.9506, 'longitude': -82.4572},
    {'full_name': 'Jacksonville Riverside Motors', 'short_name': 'Riverside', 'city': 'Jacksonville', 'state': 'FL', 'zip_code': '32202', 'address': '117 W Duval St', 'phone': '555-0504', 'email': 'sales@riverside.com', 'latitude': 30.3322, 'longitude': -81.6557},
    # Illinois (3)
    {'full_name': 'Chicago Windy City Cars', 'short_name': 'Windy City', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601', 'address': '100 Michigan Ave', 'phone': '555-0601', 'email': 'sales@windycity.com', 'latitude': 41.8781, 'longitude': -87.6298},
    {'full_name': 'Springfield Prairie Motors', 'short_name': 'Prairie', 'city': 'Springfield', 'state': 'IL', 'zip_code': '62701', 'address': '1 Capitol Ave', 'phone': '555-0602', 'email': 'sales@prairie.com', 'latitude': 39.7817, 'longitude': -89.6501},
    {'full_name': 'Naperville Suburban Auto', 'short_name': 'Suburban', 'city': 'Naperville', 'state': 'IL', 'zip_code': '60540', 'address': '400 S Eagle St', 'phone': '555-0603', 'email': 'sales@suburban.com', 'latitude': 41.7859, 'longitude': -88.1473},
    # Ohio (3)
    {'full_name': 'Columbus Buckeye Motors', 'short_name': 'Buckeye', 'city': 'Columbus', 'state': 'OH', 'zip_code': '43215', 'address': '90 W Broad St', 'phone': '555-0701', 'email': 'sales@buckeye.com', 'latitude': 39.9612, 'longitude': -82.9988},
    {'full_name': 'Cleveland Rock & Roll Cars', 'short_name': 'Rock Roll', 'city': 'Cleveland', 'state': 'OH', 'zip_code': '44113', 'address': '1500 W 3rd St', 'phone': '555-0702', 'email': 'sales@rockroll.com', 'latitude': 41.4993, 'longitude': -81.6944},
    {'full_name': 'Cincinnati Queen City Auto', 'short_name': 'Queen City', 'city': 'Cincinnati', 'state': 'OH', 'zip_code': '45202', 'address': '801 Plum St', 'phone': '555-0703', 'email': 'sales@queencity.com', 'latitude': 39.1031, 'longitude': -84.5120},
    # Pennsylvania (2)
    {'full_name': 'Philadelphia Liberty Motors', 'short_name': 'Liberty', 'city': 'Philadelphia', 'state': 'PA', 'zip_code': '19102', 'address': '1500 Market St', 'phone': '555-0801', 'email': 'sales@liberty.com', 'latitude': 39.9526, 'longitude': -75.1652},
    {'full_name': 'Pittsburgh Steel City Cars', 'short_name': 'Steel City', 'city': 'Pittsburgh', 'state': 'PA', 'zip_code': '15222', 'address': '501 Grant St', 'phone': '555-0802', 'email': 'sales@steelcity.com', 'latitude': 40.4406, 'longitude': -79.9959},
    # Georgia (2)
    {'full_name': 'Atlanta Peach State Auto', 'short_name': 'Peach State', 'city': 'Atlanta', 'state': 'GA', 'zip_code': '30303', 'address': '55 Trinity Ave', 'phone': '555-0901', 'email': 'sales@peachstate.com', 'latitude': 33.7490, 'longitude': -84.3880},
    {'full_name': 'Savannah River Street Motors', 'short_name': 'River Street', 'city': 'Savannah', 'state': 'GA', 'zip_code': '31401', 'address': '115 E River St', 'phone': '555-0902', 'email': 'sales@riverstreet.com', 'latitude': 32.0809, 'longitude': -81.0912},
    # North Carolina (2)
    {'full_name': 'Charlotte Queen City Motors', 'short_name': 'QC Charlotte', 'city': 'Charlotte', 'state': 'NC', 'zip_code': '28202', 'address': '100 Tryon St', 'phone': '555-1001', 'email': 'sales@qccharlotte.com', 'latitude': 35.2271, 'longitude': -80.8431},
    {'full_name': 'Raleigh Research Triangle Cars', 'short_name': 'Research Tri', 'city': 'Raleigh', 'state': 'NC', 'zip_code': '27601', 'address': '1 E Morgan St', 'phone': '555-1002', 'email': 'sales@researchtri.com', 'latitude': 35.7796, 'longitude': -78.6382},
    # Michigan (2)
    {'full_name': 'Detroit Motor City Cars', 'short_name': 'Motor City', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48201', 'address': '2 Woodward Ave', 'phone': '555-1101', 'email': 'sales@motorcity.com', 'latitude': 42.3314, 'longitude': -83.0458},
    {'full_name': 'Grand Lakeshore Motors', 'short_name': 'Lakeshore', 'city': 'Grand Rapids', 'state': 'MI', 'zip_code': '49503', 'address': '300 Monroe Ave', 'phone': '555-1102', 'email': 'sales@lakeshore.com', 'latitude': 42.9634, 'longitude': -85.6681},
    # Washington (2)
    {'full_name': 'Seattle Emerald City Cars', 'short_name': 'Emerald City', 'city': 'Seattle', 'state': 'WA', 'zip_code': '98101', 'address': '600 4th Ave', 'phone': '555-1201', 'email': 'sales@emeraldcity.com', 'latitude': 47.6062, 'longitude': -122.3321},
    {'full_name': 'Spokane Lilac City Motors', 'short_name': 'Lilac City', 'city': 'Spokane', 'state': 'WA', 'zip_code': '99201', 'address': '808 W Spokane Falls Blvd', 'phone': '555-1202', 'email': 'sales@lilaccity.com', 'latitude': 47.6588, 'longitude': -117.4260},
    # Colorado (2)
    {'full_name': 'Denver Mile High Motors', 'short_name': 'Mile High', 'city': 'Denver', 'state': 'CO', 'zip_code': '80202', 'address': '1700 Lincoln St', 'phone': '555-1301', 'email': 'sales@milehigh.com', 'latitude': 39.7392, 'longitude': -104.9903},
    {'full_name': 'Boulder Front Range Cars', 'short_name': 'Front Range', 'city': 'Boulder', 'state': 'CO', 'zip_code': '80302', 'address': '1300 Pearl St', 'phone': '555-1302', 'email': 'sales@frontrange.com', 'latitude': 40.0150, 'longitude': -105.2705},
    # Massachusetts (2)
    {'full_name': 'Boston Bay State Motors', 'short_name': 'Bay State', 'city': 'Boston', 'state': 'MA', 'zip_code': '02108', 'address': '1 Beacon St', 'phone': '555-1401', 'email': 'sales@baystate.com', 'latitude': 42.3601, 'longitude': -71.0589},
    {'full_name': 'Cambridge Harvard Square Cars', 'short_name': 'Harvard Sq', 'city': 'Cambridge', 'state': 'MA', 'zip_code': '02138', 'address': '10 Brattle St', 'phone': '555-1402', 'email': 'sales@harvardsq.com', 'latitude': 42.3736, 'longitude': -71.1097},
    # Virginia (2)
    {'full_name': 'Richmond Capitol Motors', 'short_name': 'Capitol', 'city': 'Richmond', 'state': 'VA', 'zip_code': '23219', 'address': '900 E Main St', 'phone': '555-1501', 'email': 'sales@capitol.com', 'latitude': 37.5407, 'longitude': -77.4360},
    {'full_name': 'Virginia Beach Oceanfront Cars', 'short_name': 'Oceanfront', 'city': 'Virginia Beach', 'state': 'VA', 'zip_code': '23451', 'address': '2100 Atlantic Ave', 'phone': '555-1502', 'email': 'sales@oceanfront.com', 'latitude': 36.8529, 'longitude': -75.9780},
    # Arizona (2)
    {'full_name': 'Phoenix Valley of the Sun Motors', 'short_name': 'Valley Sun', 'city': 'Phoenix', 'state': 'AZ', 'zip_code': '85003', 'address': '200 W Washington St', 'phone': '555-1601', 'email': 'sales@valleysun.com', 'latitude': 33.4484, 'longitude': -112.0740},
    {'full_name': 'Tucson Sonoran Desert Cars', 'short_name': 'Sonoran', 'city': 'Tucson', 'state': 'AZ', 'zip_code': '85701', 'address': '100 N Stone Ave', 'phone': '555-1602', 'email': 'sales@sonoran.com', 'latitude': 32.2226, 'longitude': -110.9747},
    # Nevada (1)
    {'full_name': 'Las Vegas Strip Motors', 'short_name': 'Strip', 'city': 'Las Vegas', 'state': 'NV', 'zip_code': '89101', 'address': '3900 Las Vegas Blvd S', 'phone': '555-1701', 'email': 'sales@strip.com', 'latitude': 36.1699, 'longitude': -115.1398},
    # Oregon (1)
    {'full_name': 'Portland Rose City Motors', 'short_name': 'Rose City', 'city': 'Portland', 'state': 'OR', 'zip_code': '97201', 'address': '1000 SW Broadway', 'phone': '555-1801', 'email': 'sales@rosecity.com', 'latitude': 45.5152, 'longitude': -122.6784},
    # Minnesota (1)
    {'full_name': 'Minneapolis City of Lakes Cars', 'short_name': 'City Lakes', 'city': 'Minneapolis', 'state': 'MN', 'zip_code': '55401', 'address': '350 S 5th St', 'phone': '555-1901', 'email': 'sales@citylakes.com', 'latitude': 44.9778, 'longitude': -93.2650},
    # Tennessee (1)
    {'full_name': 'Nashville Music City Motors', 'short_name': 'Music City', 'city': 'Nashville', 'state': 'TN', 'zip_code': '37201', 'address': '1 Public Sq', 'phone': '555-2001', 'email': 'sales@musiccity.com', 'latitude': 36.1627, 'longitude': -86.7816},
    # Maryland (1)
    {'full_name': 'Baltimore Charm City Motors', 'short_name': 'Charm City', 'city': 'Baltimore', 'state': 'MD', 'zip_code': '21201', 'address': '100 N Charles St', 'phone': '555-2101', 'email': 'sales@charmcity.com', 'latitude': 39.2904, 'longitude': -76.6122},
    # Wisconsin (1)
    {'full_name': 'Milwaukee Brew City Motors', 'short_name': 'Brew City', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53202', 'address': '200 E Wells St', 'phone': '555-2201', 'email': 'sales@brewcity.com', 'latitude': 43.0389, 'longitude': -87.9065},
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

        # ----- Reviews (idempotent: key on (dealer, name) so re-runs don't duplicate) -----
        dealers = list(Dealer.objects.all())
        makes = list(CarMake.objects.prefetch_related('car_models').all())
        for i, (name, text, purchased, year) in enumerate(SAMPLE_REVIEWS):
            dealer = dealers[i % len(dealers)]
            make = makes[i % len(makes)]
            model = list(make.car_models.all())[0]
            sentiment, _ = analyze_sentiment(text)
            Review.objects.update_or_create(
                dealer=dealer, name=name,
                defaults={
                    'review_text': text,
                    'purchase': purchased, 'car_year': year,
                    'car_make': make, 'car_model': model, 'sentiment': sentiment,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Created/updated {len(SAMPLE_REVIEWS)} reviews'))

        self.stdout.write(self.style.SUCCESS('=== Seed complete ==='))
