import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check, Channel
from hc.accounts.models import Member
from django.db.models import Q

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(Q(alert_after__gt=now, status="down")|Q(alert_after__gt=now, status="down-ext"))
        nag = query.filter(Q(nag_after__lt=now, nag_status=True, status="down")|Q(nag_after__lt=now, nag_status=True, status="down-ext"))
        going_down_ext = query.filter(alert_stay_down__lt=now, nag_status=False ,status='down')
        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + list(going_up.iterator()) + list(nag.iterator()) + list(going_down_ext.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        now = timezone.now()
        check.status = check.get_status()
        if check.nag() == 'nag':
            interval = check.timeout + check.grace
            check.nag_after = now + interval
        check.save()
        
        if check.status in ('up', 'down-ext') or check.nag() == 'nag':
            self.send_mail(check, None)
        else:
            members = Member.objects.filter(team=check.user.profile).all()
            for member in members:
                if member.team_priority and check.code in [check.code for check in member.checks.all()]:
                    self.send_mail(check, member.user.email)

        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)

    def send_mail(self, check, contact):
        '''Function to send an email to a check'''
        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert(contact)
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" % (ch.kind, ch.value, error))
