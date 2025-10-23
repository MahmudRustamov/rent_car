from django.core.management.base import BaseCommand

from apps.cars.models import Car


class Command(BaseCommand):
    help = 'Add 20 sample cars to the database'

    def handle(self, *args, **kwargs):
        cars_data = [
            {"brand": "Toyota", "model": "Camry", "year": 2023, "price_per_day": 45.00,
             "description": "Reliable sedan with great fuel economy"},
            {"brand": "Honda", "model": "Civic", "year": 2022, "price_per_day": 40.00,
             "description": "Compact car perfect for city driving"},
            {"brand": "Ford", "model": "Mustang", "year": 2024, "price_per_day": 85.00,
             "description": "Iconic sports car with powerful performance"},
            {"brand": "Chevrolet", "model": "Malibu", "year": 2023, "price_per_day": 42.00,
             "description": "Comfortable midsize sedan"},
            {"brand": "BMW", "model": "3 Series", "year": 2023, "price_per_day": 95.00,
             "description": "Luxury sedan with premium features"},
            {"brand": "Mercedes-Benz", "model": "C-Class", "year": 2024, "price_per_day": 110.00,
             "description": "Executive sedan with elegant design"},
            {"brand": "Audi", "model": "A4", "year": 2023, "price_per_day": 100.00,
             "description": "Sophisticated sedan with advanced technology"},
            {"brand": "Tesla", "model": "Model 3", "year": 2024, "price_per_day": 90.00,
             "description": "Electric sedan with autopilot features"},
            {"brand": "Nissan", "model": "Altima", "year": 2022, "price_per_day": 38.00,
             "description": "Affordable family sedan"},
            {"brand": "Mazda", "model": "CX-5", "year": 2023, "price_per_day": 55.00,
             "description": "Stylish compact SUV"},
            {"brand": "Hyundai", "model": "Tucson", "year": 2023, "price_per_day": 50.00,
             "description": "Versatile SUV with modern amenities"},
            {"brand": "Kia", "model": "Sportage", "year": 2024, "price_per_day": 52.00,
             "description": "Compact SUV with bold styling"},
            {"brand": "Volkswagen", "model": "Jetta", "year": 2022, "price_per_day": 43.00,
             "description": "German-engineered compact sedan"},
            {"brand": "Subaru", "model": "Outback", "year": 2023, "price_per_day": 60.00,
             "description": "Adventure-ready wagon with AWD"},
            {"brand": "Jeep", "model": "Wrangler", "year": 2024, "price_per_day": 75.00,
             "description": "Off-road capable SUV"},
            {"brand": "Toyota", "model": "RAV4", "year": 2023, "price_per_day": 58.00,
             "description": "Popular compact SUV"},
            {"brand": "Honda", "model": "CR-V", "year": 2024, "price_per_day": 62.00,
             "description": "Spacious and reliable SUV"},
            {"brand": "Ford", "model": "Explorer", "year": 2023, "price_per_day": 70.00,
             "description": "Three-row family SUV"},
            {"brand": "Chevrolet", "model": "Equinox", "year": 2022, "price_per_day": 48.00,
             "description": "Practical compact SUV"},
            {"brand": "Lexus", "model": "ES 350", "year": 2024, "price_per_day": 120.00,
             "description": "Luxury sedan with exceptional comfort"},
        ]

        created_count = 0
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(
                brand=car_data['brand'],
                model=car_data['model'],
                year=car_data['year'],
                defaults=car_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {car}'))
            else:
                self.stdout.write(self.style.WARNING(f'- Already exists: {car}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully added {created_count} new cars!'))