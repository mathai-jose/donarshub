from django.core.management.base import BaseCommand
from Admin.models import *
from Donar.models import *
from Guest.models import *
from Recipient.models import *

class Command(BaseCommand):
    help = 'Clears all user-related data from the system'

    def handle(self, *args, **options):
        # Clear Donors (New, Accepted, Rejected lists are managed by status field)
        tbl_donar.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all donor data'))

        # Clear Recipients (Organizations)
        tbl_recipient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all recipient data'))

        # Clear related data
        tbl_applyrequirements.objects.all().delete()
        tbl_requirements.objects.all().delete()
        tbl_appointments.objects.all().delete()
        tbl_events.objects.all().delete()
        tbl_complaint.objects.all().delete()
        tbl_feedback.objects.all().delete()
        Chat.objects.all().delete()
        tbl_paymentrecord.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All user data has been cleared successfully'))
