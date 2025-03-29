from django.core.management.base import BaseCommand
from Guest.models import tbl_donar, tbl_recipient
from Recipient.models import tbl_requirements, Chat, tbl_events
from Donar.models import tbl_applyrequirements, tbl_paymentrecord, tbl_appointments
import os
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Reset all user data while preserving system configuration'

    def handle(self, *args, **kwargs):
        try:
            # Clear all user-related data
            self.stdout.write('Clearing user data...')
            
            # Delete all appointments
            tbl_appointments.objects.all().delete()
            self.stdout.write('- Cleared appointments')
            
            # Delete all payments
            tbl_paymentrecord.objects.all().delete()
            self.stdout.write('- Cleared payment records')
            
            # Delete all requirement applications
            tbl_applyrequirements.objects.all().delete()
            self.stdout.write('- Cleared requirement applications')
            
            # Delete all chat messages
            Chat.objects.all().delete()
            self.stdout.write('- Cleared chat messages')
            
            # Delete all events
            tbl_events.objects.all().delete()
            self.stdout.write('- Cleared events')
            
            # Delete all requirements
            tbl_requirements.objects.all().delete()
            self.stdout.write('- Cleared requirements')
            
            # Delete all donors
            tbl_donar.objects.all().delete()
            self.stdout.write('- Cleared donor data')
            
            # Delete all recipients
            tbl_recipient.objects.all().delete()
            self.stdout.write('- Cleared recipient data')
            
            # Clear uploaded files
            docs_path = os.path.join(settings.MEDIA_ROOT, 'docs')
            if os.path.exists(docs_path):
                shutil.rmtree(docs_path)
                os.makedirs(docs_path)
                self.stdout.write('- Cleared uploaded files')
            
            self.stdout.write(self.style.SUCCESS('Successfully reset all user data'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
