import csv
from django.core.management.base import BaseCommand
from accounts.models import Skill  # replace with your actual app/model

class Command(BaseCommand):
    help = 'Import skills from CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'skills.csv'  # path to your CSV

        skill_objects = []
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                skill_name = row['name'].strip()
                if skill_name:
                    skill_objects.append(Skill(name=skill_name))

        Skill.objects.bulk_create(skill_objects, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"{len(skill_objects)} skills added successfully!"))
