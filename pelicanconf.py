#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
#######################################################################
#                               GENERAL                               #
#######################################################################

AUTHOR = 'Michael Medin'
SITENAME = 'NSClient++'
SITESUBTITLE = 'A modern monitoring agent'
STARTING_YEAR = 2005
SITEURL = ''
DEBUG = True

THEME = "themes/nsclient-pelican-theme"
PLUGIN_PATHS = ['plugins/pelican-plugins', 'plugins/pelican_youtube', 'plugins']
PLUGINS = [
    "pelican-bootstrapify", 
    "liquid_tags", 
    "liquid_tags.youtube", 
    "pelican_youtube", 
    "sitemap", 
    "pelican-page-hierarchy", 
    "pelican-page-order", 
    "assets", 
    "autostatic", 
    "autostatic", 
    "summary", 
    "clean_summary",
    "neighbors",
    "related_posts",
    "pelican-advthumbnailer",
    "tipue_search",
    "share_post",
    "tag_cloud",
    "pelican-github-releases"
    ]

PATH = "content"


DEFAULT_DATE_FORMAT = '%Y-%m-%d'
TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

GITHUB_RELEASE_URL = 'https://api.github.com/repos/mickem/nscp/releases'
GITHUB_MAJOR_VERSIONS = [ '0.4.3', '0.4.4', '0.5.0']
GITHUB_PROMOTED_VERSION = '0.4.3.143'
GITHUB_RELEASE_SAVE_AS = 'download/{version}/index.html'
GITHUB_RELEASE_PROMOTED_SAVE_AS = 'download/index.html'

MENUITEMS = [
	('NSClient++', '/nsclient/'),
	('News', '/blog/'),
	('Download', '/download/'),
	('Documentation', 'https://docs.nsclient.org'),
	('Support', '/support'),
	('Forums', 'https://forums.nsclient.org')
	]
	
SUBMENUITEMS = {
	'NSClient++': [
		('About NSCLient++', '/nsclient/'),
		('Sponsors', '/nsclient/sponsor/'),
		('Become a sponsor', '/nsclient/become-a-sponsor/'),
		('About the author', '/nsclient/author/')
	],
    'Download':  [
		('Latest', '/download'),
		('0.4.3', '/download/0.4.3/'),
		('0.4.4', '/download/0.4.4/'),
		('0.5.0', '/download/0.5.0/')
    ],
    'Support': [
        ('Support', '/support/'),
        ('Comercial Support Portal', 'https://nsclient.freshdesk.com/helpdesk'),
        ('Community support Portal', 'https://github.com/mickem/nscp/issues')
    ]
}
DISPLAY_PAGES_ON_MENU = False
DISPLAY_ARCHIVES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

INDEX_SAVE_AS = 'blog/index.html'
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
ARCHIVES_URL = 'archive'
ARCHIVES_SAVE_AS = 'archive/index.html'
CATEGORIES_URL = 'category'
CATEGORIES_SAVE_AS = 'category/index.html'
AUTHORS_URL = 'authors'
AUTHORS_SAVE_AS = 'authors/index.html'
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
TAGS_URL = 'tag'
TAGS_SAVE_AS = 'tag/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

#PAGINATION_PATTERNS = (
#    (1, '{base_name}/', '{base_name}/index.html'),
#    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
#)


# Social widget
SOCIAL = (("Github", "https://github.com/mickem/nscp"),
          ("Facebook", "https://www.facebook.com/nsclient"),
          ("Twitter", "https://twitter.com/mickem"),)

TWITTER_USERNAME = "mickem"
TWITTER_CARD = True
OPEN_GRAPH = True
OPEN_GRAPH_ARTICLE_AUTHOR = "Michael Medin"
DEFAULT_METADESC = 'Random thoughts on development, monitoring and family life…'
DEFAULT_SOCIAL_IMAGE = 'images/michael-medin.jpg'
DEFAULT_PAGINATION = 20
FAVICON = 'images/FAVICON.PNG'
#######################################################################
#                             Contents                                #
#######################################################################

ARTICLE_PATHS = ['blog']

PATH_METADATA = r".*(?:/|\\)(?P<category>[^/\\]+)(?:/|\\)(?P<date>\d{4}-\d{2}-\d{2})(?:/|\\)(?P<slug>[^/\\]+)(?:/|\\).*"
USE_FOLDER_AS_CATEGORY=False

PAGE_PATHS = ['pages']

GOOGLE_SEARCH = "009388823403057951110:jwq9vehc3_q"

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
SLUGIFY_SOURCE = 'basename'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'

THEME_DEVELOPMENT = True

#######################################################################
#                             Extensions                              #
#######################################################################

DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives', 'sponsor']

MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra']

SKIP_COLOPHON= True

RELATED_POSTS_MAX = 5
CLEAN_SUMMARY_MAXIMUM = 0

CUSTOM_SCRIPTS_BASE = 'add_sponsor.html'

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
