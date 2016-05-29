# coding=utf-8
#
# a part of mearie.org

import sys
import sqlite3

if len(sys.argv) < 2:
    print >>sys.stderr, 'Usage: %s <db path>' % sys.argv[0]
    raise SystemExit(1)

VERSION = 1

db = sqlite3.connect(sys.argv[1])
ver, = db.execute('pragma user_version').fetchone()
if ver == 0: # no schema
    db.executescript('''
        pragma user_version = ''' + str(VERSION) + ''';
        create table pages(
            stem text not null collate binary,
            lang text,
            short text collate binary,
            parent text,
            title text,
            date text, -- ISO 8601 partial/complete date and/or time
            "order" text collate binary, -- used for navigation generation
            summary text,
            primary key (stem, lang),
            unique ("order", lang)
        );
        create index pages_lang on pages(lang, stem);
        create table redirects(
            stem text not null collate binary,
            lang text,
            target text not null collate binary,
            primary key (stem, lang),
            foreign key (target, lang) references pages(stem, lang)
        );
        create index redirects_lang on pages(lang, stem);
    ''')
elif ver != VERSION:
    print >>sys.stderr, \
        'cannot update the database schema (latest %r, given %r)' % (VERSION, ver)
    raise SystemExit(1)
db.commit()
db.close()

