from datetime import datetime
from django.db.models import Exists, OuterRef, Q

import pytz
from django.contrib.admin.models import LogEntry
from django.core.management import call_command
from django.core.management.base import BaseCommand
from impersonate.models import ImpersonationLog
from juntagrico.entity.jobs import Assignment, Job, OneTimeJob, RecuringJob
from juntagrico.entity.subs import Subscription
from juntagrico.entity.share import Share
from juntagrico.entity.member import Member, SubscriptionMembership
from juntagrico_custom_sub.entity.subscription_content import SubscriptionContent
from juntagrico_custom_sub.entity.subscription_content_future_item import (
    SubscriptionContentFutureItem,
)
from juntagrico_custom_sub.entity.subscription_content_item import (
    SubscriptionContentItem,
)


class Command(BaseCommand):
    def handle(self, *args, **options):

        confirm = (
            input("This will delete data in the currently configured database. Type CONFIRM to proceed:\n") == "CONFIRM"
        )

        if confirm:
            start_of_year = datetime(datetime.today().year, 1, 1, tzinfo=pytz.UTC)
            cancellation_limit = datetime(datetime.today().year - 1, 9, 30, tzinfo=pytz.UTC)

            call_command("clearsessions")

            impersonation_logs = ImpersonationLog.objects.all().delete()
            print("deleted impersonation logs: ", impersonation_logs[0])

            admin_logs = LogEntry.objects.all().delete()
            print("deleted admin logs: ", admin_logs[0])

            # TODO: potentially use polymorphic api: https://django-polymorphic.readthedocs.io/en/stable/
            assignments = Assignment.objects.filter(job__time__lte=start_of_year).delete()
            print("deleted assignments: ", assignments[0])

            one_time_jobs = OneTimeJob.objects.filter(time__lte=start_of_year).delete()
            print("deleted one-time jobs: ", one_time_jobs[0])

            recurring_jobs = RecuringJob.objects.filter(time__lte=start_of_year).delete()
            print("deleted recurring jobs: ", recurring_jobs[0])

            jobs = Job.objects.filter(time__lte=start_of_year).delete()
            print("deleted jobs: ", jobs[0])

            subscription_content_items = SubscriptionContentItem.objects.filter(
                subscription_content__subscription__cancellation_date__lte=cancellation_limit
            ).delete()
            print("deleted subscription content items: ", subscription_content_items[0])

            subscription_content_future_items = SubscriptionContentFutureItem.objects.filter(
                subscription_content__subscription__cancellation_date__lte=cancellation_limit
            ).delete()
            print(
                "deleted subscription content future items: ",
                subscription_content_future_items[0],
            )

            subscription_contents = SubscriptionContent.objects.filter(
                subscription__cancellation_date__lte=cancellation_limit
            ).delete()
            print(
                "deleted subscription contents: ",
                subscription_contents[0],
            )

            subscriptions = Subscription.objects.filter(cancellation_date__lte=cancellation_limit).delete()
            print(
                "deleted subscriptions: ",
                subscriptions[0],
            )

            shares = Share.objects.filter(payback_date__lte=start_of_year).delete()
            print(
                "deleted shares: ",
                shares[0],
            )

            members = Member.objects.filter(
                Q(~Exists(Share.objects.filter(member=OuterRef("pk"))))
                & Q(~Exists(SubscriptionMembership.objects.filter(member=OuterRef("pk"))))
            ).delete()
            print(
                "deleted members: ",
                members[0],
            )

            # users = User.objects.filter(~Exists(Member.objects.filter(user=OuterRef("pk"))))
        else:
            print("operation cancelled")
