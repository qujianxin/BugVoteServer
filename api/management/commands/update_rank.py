__author__ = 'hason'

from django.core.management.base import BaseCommand
from api.base_funcs import users


class Command(BaseCommand):
    help = "更新排名信息"

    def handle(self, *args, **options):
        count = 1
        user_rank = users.get_order_users("bonus")

        for user in user_rank:
            user.rank = count
            count += 1
            user.save()
