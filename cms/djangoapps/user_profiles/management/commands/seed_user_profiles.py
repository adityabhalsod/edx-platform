"""
Management command to seed fake user profiles.

Usage:
    ./manage.py cms seed_user_profiles
    ./manage.py cms seed_user_profiles --count 20
"""

import random
import string
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cms.djangoapps.user_profiles.models import UserProfile

User = get_user_model()

# Sample data for generating realistic profiles
FIRST_NAMES = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Edward",
    "Fiona",
    "George",
    "Hannah",
    "Ivan",
    "Julia",
    "Kevin",
    "Laura",
    "Michael",
    "Nina",
    "Oscar",
    "Patricia",
    "Quentin",
    "Rachel",
    "Samuel",
    "Tanya",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
]

CITIES = [
    "New York",
    "London",
    "Tokyo",
    "Paris",
    "Berlin",
    "Mumbai",
    "Sydney",
    "Toronto",
    "Dubai",
    "Singapore",
    "San Francisco",
    "Amsterdam",
    "Seoul",
    "Barcelona",
    "Melbourne",
]

COUNTRIES = [
    "United States",
    "United Kingdom",
    "Japan",
    "France",
    "Germany",
    "India",
    "Australia",
    "Canada",
    "UAE",
    "Singapore",
    "United States",
    "Netherlands",
    "South Korea",
    "Spain",
    "Australia",
]

BIOS = [
    "Passionate learner exploring new technologies.",
    "Software engineer with a love for open-source education.",
    "Student interested in data science and machine learning.",
    "Educator and lifelong learner.",
    "Product manager transitioning into tech.",
    "Researcher in artificial intelligence and robotics.",
    "Full-stack developer eager to learn new frameworks.",
    "Business analyst looking to upskill in Python.",
    "UX designer passionate about accessible education.",
    "DevOps engineer exploring cloud architectures.",
]


def generate_phone():
    """Generate a random phone number."""
    return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def generate_random_date(start_year=1970, end_year=2003):
    """Generate a random date of birth."""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Keep it safe across all months
    return date(year, month, day)


class Command(BaseCommand):
    help = "Seed the database with fake user profiles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of fake user profiles to create (default: 10)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        created = 0

        self.stdout.write(f"\n🌱 Seeding {count} fake user profiles...\n")

        for i in range(count):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=4)
            )
            username = f"{first_name.lower()}_{last_name.lower()}_{suffix}"
            email = f"{username}@example.com"

            # Create or get the User
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

            if user_created:
                user.set_password("Test@1234")
                user.save()

            # Create the UserProfile
            city_idx = random.randint(0, len(CITIES) - 1)
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "bio": random.choice(BIOS),
                    "avatar_url": f"https://i.pravatar.cc/150?u={username}",
                    "date_of_birth": generate_random_date(),
                    "phone_number": generate_phone(),
                    "city": CITIES[city_idx],
                    "country": COUNTRIES[city_idx],
                },
            )

            if profile_created:
                created += 1
                status = "✅ Created"
            else:
                status = "⏭️  Skipped (exists)"

            self.stdout.write(
                f"  {status}: {username} ({first_name} {last_name}) - {CITIES[city_idx]}, {COUNTRIES[city_idx]}"
            )

        self.stdout.write(
            f"\n🎉 Done! Created {created} new profile(s) (out of {count} requested).\n"
        )
