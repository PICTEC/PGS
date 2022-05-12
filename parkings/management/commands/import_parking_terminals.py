import requests
import json
from django.contrib.gis.geos import fromstr
from django.core.management import call_command
from django.core.management.base import BaseCommand

from parkings.models import EnforcementDomain, ParkingTerminal


class Command(BaseCommand):
    help = "Import parking terminals"

    def add_arguments(self, parser):
        parser.add_argument(
            'address', type=str,
            help=('Addres from where get parking areas')
            )
        parser.add_argument(
            '--local',
            action='store_true',
            help=('If the address refer to file on local drive'),
            )
        parser.add_argument(
            '--srid', 
            '-s', 
            type=int, 
            default=4326,
            )
        parser.add_argument(
            '--domain', 
            '-d', 
            type=str, 
            default=None,
            )

    def handle(self, *args, **options):
        if options['domain'] is None:
            options['domain'] = EnforcementDomain.get_default_domain()
        
        if options['local']:
            #call_command('loaddata', options['address'], verbosity=0, do)
            with open(options['address'], 'r') as file:
                for terminal_dict in json.load(file):
                    terminal = ParkingTerminal.objects.update_or_create(
                        domain=options['domain'],
                        number=terminal_dict['fields']['number'],
                        name=terminal_dict['fields']['name'],
                        location=fromstr(terminal_dict['fields']['location']),
                        )    
        else:
            r = requests.get(options['address'], allow_redirects=True)
            for terminal_dict in r.json():
                terminal = ParkingTerminal.objects.update_or_create(
                        domain=options['domain'],
                        number=terminal_dict['fields']['number'],
                        name=terminal_dict['fields']['name'],
                        location=fromstr(terminal_dict['fields']['location']),
                        )
