from scraper import Scraper
import csv

body_config = {
    'path': [
        {
            'selector': 'table',
            'options': {'class': 'forumline'}
        },
    ],
    'selector': 'tr',
    'options': {}
}

data_config = {
    'post_id': {
        'path': [ 
            { 'selector': 'span', 'options': { 'class': 'name' } } 
        ],
        'selector': 'a',
        'options': {},
        'attribute': 'name',
        'transform': lambda x: x[0]
    },
    'user_name': {
        'path': [
            { 'selector': 'span', 'options': { 'class': 'name' } } 
        ],
        'selector': 'b',
        'options': {},
        'attribute': 'text',
        'transform': lambda x: x[0]
    },
    'post_date': {
        'path': [
            { 'selector': 'td', 'options': { 'width': '100%' } } 
        ],
        'selector': 'span',
        'options': {'class': 'postdetails'},
        'attribute': 'text',
        'transform': lambda x: ' '.join(x[0].split(' ')[1:6])
    },
    'post_body': {
        'path': [],
        'selector': 'span',
        'options': { 'class': 'postbody' },
        'attribute': 'text',
        'transform': lambda x: '\n'.join(x)
    },
    'quote': {
        'path': [],
        'selector': 'td',
        'options': { 'class': 'quote' },
        'attribute': 'text',
        'transform': lambda x: '\n'.join(x) if x else ''
    }
}

nav_config = {
    'path': [
        { 'selector': 'td', 'options': {'align': 'right'} },
        { 'selector': 'span', 'options': {'class': 'nav'} },
    ],
    'selector': 'a',
    'options': {},
    'attribute': 'href'
}

scraper = Scraper('http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/', 5)
data = scraper.scrape('viewtopic.php?t=12591', body_config, nav_config, data_config)

with open ("output.csv", "wb") as outfile:
    writer = csv.writer(outfile)
    fields = data_config.keys()
    writer.writerow(fields)
    for record in data:
        row_data = [ record.get(field, '').encode('utf-8') for field in fields ]
        writer.writerow(row_data)
        