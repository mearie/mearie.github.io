# coding=utf-8
#
# a part of mearie.org
# generates a YAML file for /keywords/

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

KEYWORDS_PATH = u'w/'
lang = sys.argv[2].decode()
c = db.execute('''
    select stem, title, date from pages
    where stem like ? and lang = ? and short is not null
    order by stem asc
''', (KEYWORDS_PATH + u'%', lang,))

def word_to_group(w):
    c = (w[:1] or u'').upper()
    if u'\uac00' <= c <= u'\ud7ac':
        return u'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'[(ord(c) - 0xac00) // 588]
    elif u'0' <= c <= u'9':
        return u'0-9'
    elif u'A' <= c <= u'Z':
        return c
    else:
        return u'*'

print '[{"unMeta":{"groups":{"t":"MetaList","c":['
lastgroup = None
first = True
for stem, title, date in c:
    assert stem.startswith(KEYWORDS_PATH)
    word = stem[len(KEYWORDS_PATH):]
    if word == 'index': continue
    group = word_to_group(word)
    if group != lastgroup:
        if lastgroup: print ']}}},'
        print '{"t":"MetaMap","c":{"name":{"t":"MetaString","c":%s},"words":{"t":"MetaList","c":[' % dumps(group, separators=(',', ':'))
        lastgroup = group
        first = True
    item = {'url': {'t': 'MetaString', 'c': stem + u'.' + lang}}
    if title: item['title'] = {'t': 'MetaString', 'c': title}
    if date: item['date'] = {'t': 'MetaString', 'c': date}
    if first: first = False
    else: print ',',
    print dumps({'t': 'MetaMap', 'c': item}, separators=(',', ':'))
if lastgroup: print ']}}}'
print ']}}},[]]'
