from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import migrations
from django.contrib.gis.geos import fromstr
import requests
import json

from parkings.models import EnforcementDomain, ParkingTerminal

class Command(BaseCommand):
    help = "Import parking terminals"

    def add_arguments(self, parser):
        parser.add_argument(
            'address', type=str,
            help=('Addres from where get parking areas')
        )
        parser.add_argument(
            'local', type=str, default='False',
            help=('If the address refer to file on local drive')
        )
    def handle(self, *args, **options):
        local = options['local'].lower() in ['true', '1', 't', 'y', 'yes']
        if local:
            call_command('loaddata', options['address'], verbosity=0)
        else:
            domain = EnforcementDomain.get_default_domain()
            r = requests.get(options['address'], allow_redirects=True)
            for terminal_dict in r.json():
                terminal = ParkingTerminal.objects.update_or_create(
                    domain=domain,
                    number=terminal_dict['fields']['number'],
                    name=terminal_dict['fields']['name'],
                    location=fromstr(terminal_dict['fields']['location'], srid=4326),
                )
