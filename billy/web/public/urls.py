from django.conf.urls.defaults import patterns, url

from billy.web.public.views.misc import VotesList, NewsList
from billy.web.public.views.bills import BillList, AllBillList, BillFeed
from billy.web.public.views.region import ShowMoreLegislators
from billy.web.public.feeds import VotesListFeed, NewsListFeed, EventsFeed

# misc. views
urlpatterns = patterns(
    'billy.web.public.views.misc',

    url(r'^$', 'homepage', name='homepage'),
    url(r'^downloads/$', 'downloads', name='downloads'),
    url(r'^find_your_legislator/$', 'find_your_legislator',
        name='find_your_legislator'),
    url(r'^get_district/(?P<district_id>.+)/$', 'get_district',
        name='get_district'),

    # votes & news
    url(r'^(?P<abbr>[a-z-]+)/(?P<collection_name>[\w-]+)/(?P<_id>[\w-]+)/'
        '(?P<slug>[^/]+)/news/$',
        NewsList.as_view(), name='news_list'),
    url(r'^(?P<abbr>[a-z-]+)/(?P<collection_name>[\w-]+)/(?P<_id>[\w-]+)/'
        '(?P<slug>[^/]+)/news/rss/$',
        NewsListFeed(), name='news_list_rss'),
    url(r'^(?P<abbr>[a-z-]+)/(?P<collection_name>[\w-]+)'
        '/(?P<_id>[\w-]+)/votes/$', VotesList.as_view(), name='votes_list'),
    url(r'^(?P<abbr>[a-z-]+)/(?P<collection_name>[\w-]+)/(?P<_id>[\w-]+)/'
        'votes/rss/$',
        VotesListFeed(), name='votes_list_rss'),

)

# user-related views
urlpatterns += patterns(
    '',

    # delete this once real login lands
    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'billy/web/public/login.html'}
    ),

    url(r'^profile/$', 'billy.web.public.views.misc.user_profile',
        name='user_profile'),
    url(r'^get_user_latlong/$', 'billy.web.public.views.misc.get_user_latlong',
        name='get_user_latlong'),
    url(r'^favorites/$', 'billy.web.public.views.favorites.favorites',
        name='user_favorites'),
    url(r'^favorites/set_favorite/$',
        'billy.web.public.views.favorites.set_favorite',
        name='set_favorite'),
    url(r'^favorites/set_notification_preference/$',
        'billy.web.public.views.favorites.set_notification_preference',
        name='set_notification_preference'),
)

# region specific
urlpatterns += patterns(
    'billy.web.public.views.region',

    url(r'^(?P<abbr>[a-z-]+)/search/$', 'search', name='search'),
    url(r'^(?P<abbr>[a-z-]+)/search/show_more_legislators/$',
        ShowMoreLegislators.as_view(), name='show_more_legislators'),
    url(r'^(?P<abbr>[a-z-]+)/$', 'region', name='region'),
    url(r'^region_selection/$', 'region_selection', name='region_selection'),
)

# agendas 
urlpatterns += patterns(
    'billy.web.public.views.agendas',

    url(r'^(?P<abbr>[a-z-]+)/agendas/$', 'agendas',
        name='agendas'),
    #url(r'^(?P<abbr>[a-z-]+)/agendas/rss/$', AgendasFeed(),
    #    name='agendas_rss'),
    url(r'^(?P<abbr>[a-z-]+)/agendas/(?P<agenda_id>[\w-]+)/', 'agenda',
        name='agenda'),
    url(r'^(?P<abbr>[a-z-]+)/ical/(?P<agenda_id>[\w-]+)/', 'agenda_ical',
        name='agenda_ical'),
)

# events
urlpatterns += patterns(
    'billy.web.public.views.events',

    url(r'^(?P<abbr>[a-z-]+)/events/$', 'events',
        name='events'),
    url(r'^(?P<abbr>[a-z-]+)/events/rss/$', EventsFeed(),
        name='events_rss'),
    url(r'^(?P<abbr>[a-z-]+)/events/(?P<event_id>[\w-]+)/', 'event',
        name='event'),
    url(r'^(?P<abbr>[a-z-]+)/ical/(?P<event_id>[\w-]+)/', 'event_ical',
        name='event_ical'),
)

# committees
urlpatterns += patterns(
    'billy.web.public.views.committees',

    url(r'^(?P<abbr>[a-z-]+)/committees/$', 'committees', name='committees'),
    url(r'^(?P<abbr>[a-z-]+)/committees/(?P<committee_id>[A-Z]{3}\d+)/',
        'committee', name='committee'),
)

# legislators
urlpatterns += patterns(
    'billy.web.public.views.legislators',

    url(r'^(?P<abbr>[a-z-]+)/legislators/$', 'legislators',
        name='legislators'),
    url(r'^(?P<abbr>[a-z-]+)/legislators/(?P<_id>[\w-]+)/(?P<slug>[^/]*)/$',
        'legislator', name='legislator'),
    url(r'^(?P<abbr>[a-z-]+)/legislators/(?P<_id>[\w-]+)/$',
        'legislator', name='legislator_noslug'),
)

# speeches
urlpatterns += patterns(
    'billy.web.public.views.speeches',

    url(r'^(?P<abbr>[a-z-]+)/speeches/$', 'speeches',
        name='speeches'),
    url(r'^(?P<abbr>[a-z-]+)/speeches/(?P<event_id>[\w-]+)/',
        'speeches_by_event', name='speeches_by_event'),
)

# bills
urlpatterns += patterns(
    'billy.web.public.views.bills',

    url(r'^(?P<abbr>[a-z-]+)/bills/$', BillList.as_view(), name='bills'),
    url(r'^(?P<abbr>[a-z-]+)/bills/feed/$', BillFeed.as_view(),
        name='bills_feed'),
    url(r'^(?P<abbr>all)/bills/$', AllBillList.as_view(), name='bills'),
    url(r'^(?P<abbr>[a-z-]+)/bills/(?P<session>[^/]+)/(?P<bill_id>[^/]+)/$',
        'bill', name='bill'),
    url(r'^(?P<abbr>[a-z-]+)/(?P<bill_id>[^/]+)/$',
        'bill_noslug', name='bill_noslug'),
    url(r'^(?P<abbr>[a-z-]+)/bills/(?P<session>[^/]+)/'
        r'(?P<bill_id>[^/]+)/(?P<key>documents)/$', 'all_documents',
        name='bill_all_documents'),
    url(r'^(?P<abbr>[a-z-]+)/bills/(?P<session>[^/]+)/'
        r'(?P<bill_id>[^/]+)/documents/(?P<doc_id>[\w-]+)/$', 'document',
        name='document'),
    url(r'^(?P<abbr>[a-z-]+)/bills/(?P<session>[^/]+)/'
        r'(?P<bill_id>[^/]+)/(?P<key>versions)/$', 'all_versions',
        name='bill_all_versions'),
    url(r'^(?P<abbr>[a-z-]+)/votes/(?P<vote_id>[\w-]+)/$',
        'vote', name='vote'),
)
