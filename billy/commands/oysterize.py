import csv

from billy import db
from billy.commands import BaseCommand

from oyster.client import get_configured_client

class Oysterize(BaseCommand):
    name = 'oysterize'
    help = 'send bill versions to oyster'

    def add_args(self):
        self.add_argument('states', nargs='+', help='states to oysterize')

    def handle(self, args):
        oclient = get_configured_client()
        new_bills = list(db.bills.find({'state': state,
                                        'versions.url': {'$exists': True},
                                        #'versions._oyster_id': {'$exists': False}
                                       }))
        print '%s bills with versions to oysterize' % len(new_bills)
        for bill in new_bills:
            for version in bill['versions']:
                if 'url' in version and '_oyster_id' not in version:
                    try:
                        _id = oclient.track_url(version['url'],
                                                update_mins=update_mins,
                                                name=version['name'],
                                                state=bill['state'],
                                                session=bill['session'],
                                                chamber=bill['chamber'],
                                                bill_id=bill['bill_id'],
                                                openstates_bill_id=bill['_id'])
                        #version['_oyster_id'] = _id
                    except Exception as e:
                        print e

            # save bill after updating all versions
            #db.bills.save(bill, safe=True)