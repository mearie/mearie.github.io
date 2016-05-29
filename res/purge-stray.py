# coding=utf-8
#
# a part of mearie.org

import re
import os
import os.path
import sys
import sqlite3
import unicodedata

if len(sys.argv) < 2:
    print >>sys.stderr, 'Usage: %s <db path> <stem to purge> ...' % sys.argv[0]
    raise SystemExit(1)

STEM_PATTERN = re.compile(r'^(.*)\.([a-z]{2})$')
def parse_stem(stem):
    stem = unicodedata.normalize('NFC', stem.decode('utf-8').lower())
    m = STEM_PATTERN.search(stem)
    if m: return m.group(1), m.group(2)
    else: return stem, None

def normpath(path):
    return unicodedata.normalize('NFC', os.path.normpath(path))

def glob(root):
    for path, dirs, files in os.walk(root.decode('utf-8')):
        path = os.path.relpath(path, root)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            yield normpath(os.path.join(path, f)).encode('utf-8')

SCHEMA_VERSION = 1
def open_db(dbpath):
    db = sqlite3.connect(dbpath)
    ver, = db.execute('pragma user_version').fetchone()
    assert ver == SCHEMA_VERSION, 'check-schema didn\'t really work; ver = %r' % ver
    return db

def main(dbpath, outpath, refspat, knownoutfiles):
    db = open_db(dbpath)
    knownoutfiles = set(normpath(f.decode('utf-8')).encode('utf-8') for f in knownoutfiles)

    stems2purge = []
    for outfile in glob(outpath):
        if outfile in knownoutfiles: continue
        print outfile
        os.unlink(os.path.join(outpath, outfile))
        if outfile.endswith('.html'): # also remove from indices if any
            stem = outfile[:-5]
            rawstem, lang = parse_stem(stem)
            stems2purge.append((rawstem, lang))
            try: os.makedirs(os.path.dirname(refspat.replace('%', stem)))
            except Exception: pass
            with open(refspat.replace('%', stem), 'a') as f:
                os.utime(f.name, None)
            with open(refspat.replace('%', rawstem.encode('utf-8')), 'a') as f:
                os.utime(f.name, None)

    db.executemany('delete from pages where stem = ? and lang = ?', stems2purge)
    db.commit()
    db.close()

if __name__ == '__main__':
    if len(sys.argv) < 5 or sys.argv[4] != '--':
        print >>sys.stderr, 'Usage: %s <indices db> <output path> <references pattern> -- <files to keep, relative to output path> ... > <list of files purged>' % sys.argv[0]
        raise SystemExit(1)

    _, dbpath, outpath, refspat = sys.argv[:4]
    main(dbpath, outpath, refspat, sys.argv[5:])

