import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from django.db.models import Q
from hc.api.models import Check
from hc.accounts.models import Profile, Member

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(Q(alert_after__gt=now, status="down") | Q(alert_after__gt=now,status="down-ext"))
        going_down_ext = query.filter(alert_stay_down__lt=now, status="down")
        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + list(going_up.iterator()) + list(going_down_ext.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check, now) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check, now):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        check.save()

        print(check.name, check.status)

        profile = Profile.objects.filter(user=check.user)
        members = Member.objects.filter(team=profile)
        if check.status == "up":
            self.send(check, None)
        elif check.status == "down":
            for member in members:
                if member.team_priority:
                    self.send(check, member.user.email)
        elif check.status == "down-ext":
            self.send(check, None)

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

    def send(self, check, email):
        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert(email)
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" % (ch.kind, ch.value, error))

        connection.close()
        return True