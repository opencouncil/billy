from django.core import urlresolvers
from django.template.defaultfilters import slugify, truncatewords

from billy.core import mdb as db, settings
from .base import Document
from .metadata import Metadata


class Agenda(Document):

    collection = db.agendas

    @property
    def metadata(self):
        return Metadata.get_object(self[settings.LEVEL_FIELD])

    def items(self):
        items = []
        for item in self['related_items']:
            if 'item_id' in item:
                items.append(item['item_id'])
        return db.items.find({"_id": {"$in": items}})

    def committees(self):
        committees = []
        for committee in self['participants']:
            if 'committee_id' in committee:
                committees.append(committee['committee_id'])
        return db.committees.find({"_id": {"$in": committees}})

    def get_absolute_url(self):
        slug = slugify(truncatewords(self['description'], 10))
        url = urlresolvers.reverse('agenda', args=[self[settings.LEVEL_FIELD],
                                                  self['_id']])
        return '%s%s/' % (url, slug)
