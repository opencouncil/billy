"""
    views specific to agendas
"""
import operator
import urllib
import datetime as dt
from icalendar import Calendar, Event

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.sites.models import Site


import billy
from billy.core import settings
from billy.models import db, Metadata
from billy.models.pagination import IteratorPaginator

from .utils import templatename, RelatedObjectsList


def agenda_ical(request, abbr, agenda_id):
    agenda = db.agendas.find_one({'_id': agenda_id})
    if agenda is None:
        raise Http404

    x_name = "X-BILLY"

    cal = Calendar()
    cal.add('prodid', '-//Sunlight Labs//billy//')
    cal.add('version', billy.__version__)

    cal_agenda = Event()
    cal_agenda.add('summary', agenda['description'])
    cal_agenda['uid'] = "%s@%s" % (agenda['_id'], Site.objects.all()[0].domain)
    cal_agenda.add('priority', 5)
    cal_agenda.add('dtstart', agenda['when'])
    cal_agenda.add('dtend', (agenda['when'] + dt.timedelta(hours=1)))
    cal_agenda.add('dtstamp', agenda['updated_at'])

    if "participants" in agenda:
        for participant in agenda['participants']:
            name = participant['participant']
            cal_agenda.add('attendee', name)
            if "id" in participant and participant['id']:
                cal_agenda.add("%s-ATTENDEE-ID" % (x_name), participant['id'])

    if "related_bills" in agenda:
        for bill in agenda['related_bills']:
            if "bill_id" in bill and bill['bill_id']:
                cal_agenda.add("%s-RELATED-BILL-ID" % (x_name), bill['bill_id'])

    cal.add_component(cal_agenda)
    return HttpResponse(cal.to_ical(), content_type="text/calendar")


def agenda(request, abbr, agenda_id):
    '''
    Context:
        - abbr
        - metadata
        - agenda
        - sources
        - gcal_info
        - gcal_string
        - nav_active

    Templates:
        - billy/web/public/agenda.html
    '''
    agenda = db.agendas.find_one({'_id': agenda_id})
    if agenda is None:
        raise Http404

    fmt = "%Y%m%dT%H%M%SZ"

    start_date = agenda['when'].strftime(fmt)
    duration = dt.timedelta(hours=1)
    ed = (agenda['when'] + duration)
    end_date = ed.strftime(fmt)

    gcal_info = {
        "action": "TEMPLATE",
        "text": agenda['description'].encode('utf-8'),
        "dates": "%s/%s" % (start_date, end_date),
        "details": "",
        #"location": agenda['location'].encode('utf-8'),
        "trp": "false",
        "sprop": "http://%s/" % Site.objects.all()[0].domain,
        "sprop": "name:billy"
    }
    gcal_string = urllib.urlencode(gcal_info)

    return render(request, templatename('agenda'),
                  dict(abbr=abbr,
                       metadata=Metadata.get_object(abbr),
                       agenda=agenda,
                       sources=agenda['sources'],
                       gcal_info=gcal_info,
                       gcal_string=gcal_string,
                       nav_active='agendas'))


def agendas(request, abbr):
    '''
    Context:
      - XXX: FIXME

    Templates:
        - billy/web/public/agendas.html
    '''
    recent_agendas = db.agendas.find({
        settings.LEVEL_FIELD: abbr
    }).sort("when", -1)
    agendas = recent_agendas[:30]
    recent_agendas.rewind()

    return render(request,
                  templatename('agendas'),
                  dict(abbr=abbr,
                       metadata=Metadata.get_object(abbr),
                       agendas=agendas,
                       nav_active='agendas',
                       recent_agendas=recent_agendas))
