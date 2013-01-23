import uuid

from billy.scrape import Scraper, SourcedObject


class AgendaScraper(Scraper):

    scraper_type = 'agendas'

    def scrape(self, chamber, session):
        raise NotImplementedError("AgendaScrapers must define a scrape method")

    save_agenda = Scraper.save_object


class Agenda(SourcedObject):
    def __init__(self, session, when, type,
                 description, location, end=None, **kwargs):
        super(Agenda, self).__init__('agenda', **kwargs)
        self.uuid = uuid.uuid1()  # If we need to save an agenda more than once

        self['session'] = session
        self['when'] = when
        self['type'] = type
        self['description'] = description
        self['end'] = end
        self['participants'] = []
        self['location'] = location
        self['documents'] = []
        self['related_bills'] = []
        self.update(kwargs)

    def add_document(self, name, url, type=None, mimetype=None, **kwargs):
        d = dict(name=name, url=url, **kwargs)
        if mimetype:
            d['mimetype'] = mimetype
        if not type:
            type = "other"
        d['type'] = type
        self['documents'].append(d)

    def add_related_bill(self, bill_id, **kwargs):
        kwargs.update({"bill_id": bill_id})
        self['related_bills'].append(kwargs)

    def add_participant(self,
                        type,
                        participant,
                        participant_type,
                        **kwargs):

        kwargs.update({'type': type,
                       'participant_type': participant_type,
                       'participant': participant})

        self['participants'].append(kwargs)

    def get_filename(self):
        return "%s.json" % str(self.uuid)

    def __unicode__(self):
        return "%s %s: %s" % (self['when'], self['type'], self['description'])
