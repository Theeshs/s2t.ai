import time
from typing import Any, Optional
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Waiting documents to elastic search...')