# coding=utf-8
#
# a part of mearie.org
# generates a YAML file for /index

import sys
import sqlite3
from json import loads, dumps

if len(sys.argv) < 3:
    print >>sys.stderr, 'Usage: %s <db path> <lang> > <json path>' % sys.argv[0]
    raise SystemExit(1)

VERSION = 1
db = sqlite3.connect(sys.argv[1])
ver, = db.execute('pragma user_version').fetchone()
assert ver == VERSION, 'check-schema didn\'t really work; ver = %r' % ver

lang = sys.argv[2].decode()
c = db.execute('''
    select stem, short, parent, title, date, summary from pages
    where lang = ? and short is not null and date is not null
    order by date desc, "order" desc
    limit 5
''', (lang,))

print '[{"unMeta":{"recent":{"t":"MetaList","c":['
first = True
for stem, short, parent, title, date, summary in c:
    item = {'url': {'t': 'MetaString', 'c': stem + u'.' + lang}}
    if short: item['short'] = {'t': 'MetaString', 'c': short}
    if parent: item['parent'] = loads(parent) # keep the parsed Markdown
    if title: item['title'] = {'t': 'MetaString', 'c': title}
    if date: item['date'] = {'t': 'MetaString', 'c': date}
    if summary:
        summary = loads(summary)
        assert summary['t'] == 'MetaBlocks'
        last = summary['c'] and summary['c'][-1]
        if last and last['t'] == 'RawBlock' and last['c'] == ['html', '<!-- more -->']:
            item['more'] = {'t': 'MetaString', 'c': 'more'} # print the "more" link if needed
        summary['c'].append({'t': 'RawBlock', 'c': ('html', '<!-- notes -->')}) # flush notes
        item['summary'] = summary
    if first: first = False
    else: print ',',
    print dumps({'t': 'MetaMap', 'c': item}, separators=(',', ':'))
print ']}}},[]]'

