#!/usr/bin/env python
"""
Create superuser and monitoring group
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from parkings.models import Monitor
from parkings.models import EnforcementDomain

MODELS = ['operator', 'parking area', 'parking check', 'parking terminal', 'parking', 'region', 'payment zone']
PERMISSIONS = ['view']

class Command(BaseCommand):
    help = 'Create superuser and monitor'

    def add_arguments(self, parser):
        parser.add_argument('superuser_name', type=str)
        parser.add_argument('superuser_email', type=str)
        parser.add_argument('superuser_password', type=str)

    def handle(self, superuser_name, superuser_email, superuser_password, *args, **options):
        try:
            user = User.objects.create_superuser(superuser_name, superuser_email, superuser_password)
            print("Created superuser " + superuser_name)
        except Exception as e:
            print("Failed in creating superuser " + superuser_name)
            print(e)
            return

        monitor = Monitor.objects.update_or_create(
            name=superuser_name,
            user=user,
            domain=EnforcementDomain.get_default_domain(),
        )

        print("Created monitor for superuser " + superuser_name)
