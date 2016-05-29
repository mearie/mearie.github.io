# coding=utf-8
#
# a part of mearie.org
# portions derived from pandocfilters. (C) 2013 John MacFarlane

import os
import os.path
import posixpath
import re
import sys
import time
import json
import urllib
import subprocess
import hashlib
import tempfile
import sqlite3
import unicodedata

def walk(x, action):
    """Walk a tree, applying an action to every object.
    Returns a modified tree.
    """
    if isinstance(x, list):
        array = []
        for item in x:
            if isinstance(item, dict) and 't' in item:
                res = action(item['t'], item['c'])
                if res is None:
                    array.append(walk(item, action))
                elif isinstance(res, list):
                    for z in res: array.append(walk(z, action))
                else:
                    array.append(walk(res, action))
            else:
                array.append(walk(item, action))
        return array
    elif isinstance(x, dict):
        obj = {}
        for k in x: obj[k] = walk(x[k], action)
        return obj
    elif isinstance(x, tuple):
        tup = []
        for v in x: tup.append(walk(v, action))
        return tuple(tup)
    else:
        return x

def stringify(x):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val):
        if key in ['Str', 'MetaString']:
            result.append(val)
        elif key == 'Code':
            result.append(val[1])
        elif key == 'Math':
            result.append(val[1])
        elif key == 'LineBreak':
            result.append(" ")
        elif key == 'Space':
            result.append(" ")

    walk(x, go)
    return ''.join(result)

def stringify_list(x):
    """Similar to stringify but expects the content to be a YAML list.
    If not, it returns a list of one stringified content.
    """
    if isinstance(x, dict) and x['t'] == 'MetaList':
        return map(stringify, x['c'])
    else:
        return [stringify(x)]

def attributes(attrs):
    """Returns an attribute list, constructed from the
    dictionary attrs.
    """
    attrs = attrs or {}
    ident = attrs.get("id", "")
    classes = attrs.get("classes", [])
    keyvals = [[x, attrs[x]] for x in attrs if (x != "classes" and x != "id")]
    return [ident, classes, keyvals]

def elt(eltType, numargs):
    def fun(*args):
        lenargs = len(args)
        if lenargs != numargs:
            raise ValueError(eltType + ' expects '
                             + str(numargs) + ' arguments, but given '
                             + str(lenargs))
        if numargs == 0:
            xs = []
        elif len(args) == 1:
            xs = args[0]
        else:
            xs = args
        return {'t': eltType, 'c': xs}
    return fun

# Constructors for metadata
MetaInlines = elt('MetaInlines', 1)
MetaBlocks = elt('MetaBlocks', 1)
MetaBool = elt('MetaBool', 1)
MetaString = elt('MetaString', 1)
MetaMap = elt('MetaMap', 1)
MetaList = elt('MetaList', 1)

# Constructors for block elements
Plain = elt('Plain', 1)
Para = elt('Para', 1)
CodeBlock = elt('CodeBlock', 2)
RawBlock = elt('RawBlock', 2)
BlockQuote = elt('BlockQuote', 1)
OrderedList = elt('OrderedList', 2)
BulletList = elt('BulletList', 1)
DefinitionList = elt('DefinitionList', 1)
Header = elt('Header', 3)
HorizontalRule = elt('HorizontalRule', 0)
Table = elt('Table', 5)
Div = elt('Div', 2)
Null = elt('Null', 0)

# Constructors for inline elements
Str = elt('Str', 1)
Emph = elt('Emph', 1)
Strong = elt('Strong', 1)
Strikeout = elt('Strikeout', 1)
Superscript = elt('Superscript', 1)
Subscript = elt('Subscript', 1)
SmallCaps = elt('SmallCaps', 1)
Quoted = elt('Quoted', 2)
Cite = elt('Cite', 2)
Code = elt('Code', 2)
Space = elt('Space', 0)
LineBreak = elt('LineBreak', 0)
Math = elt('Math', 2)
RawInline = elt('RawInline', 2)
Link = elt('Link', 3)
Image = elt('Image', 3)
Note = elt('Note', 1)
SoftBreak = elt('SoftBreak', 0)
Span = elt('Span', 2)


def to_json(v):
    return json.dumps(v, separators=(',', ':'))

def localize_meta(meta, lang):
    if meta['t'] == 'MetaMap':
        return meta['c'][lang]
    else:
        return meta

KEYWORDS_PATH = u'w/'
KEYWORD_SEP2DASH_PATTERN = re.compile(ur'(?<=[a-z])[^\w._]+|[^\w._]+(?=[a-z])|'
                                      ur'(?<=[a-z0-9])[^\w._]+(?=[a-z0-9])', re.U)
def normalize_keyword(word):
    word = unicodedata.normalize('NFC', word)
    word = u''.join(c if c.isalnum() or c in '._' else u' ' for c in word.lower())
    word = u''.join(KEYWORD_SEP2DASH_PATTERN.sub(u'-', word).split()).strip(u'-')
    return word

def transform(doc, stem, git):
    assert not stem.startswith('/') and not stem.endswith('/')

    # extract the language component from the path stem
    m = re.search(r'^(.*)\.([a-z]{2})$', stem.lower())
    assert m, 'no language component from the path'
    rawstem = m.group(1)
    guessed_lang = m.group(2)

    # local return context
    class ret(object): pass
    ret.rawstem = rawstem
    ret.lang = guessed_lang
    ret.template = 'main'
    ret.short = None
    ret.redirect_from = []
    ret.resources = []
    ret.parent = None
    ret.title = None
    ret.date = None
    ret.summary = None
    ret.refs = set()

    meta = doc[0]['unMeta']
    seen_self = False
    for k, v in meta.items():
        if k == 'lang':
            lang = stringify(v).lower()
            if ret.lang is not None:
                assert lang == ret.lang, \
                    'conflicting path (%r) and specified language (%r)' % (ret.lang, lang)
        elif k == 'template':
            ret.template = stringify(v)
        elif k == 'short':
            ret.short = stringify(v).strip('/')
        elif k == 'redirect-from':
            ret.redirect_from.extend(i.strip('/') for i in stringify_list(v))
        elif k == 'aliases': # redirect-from for keywords
            ret.redirect_from.extend(KEYWORDS_PATH + normalize_keyword(i) for i in stringify_list(v))
        elif k == 'resources':
            ret.resources = stringify_list(v)
        elif k == 'parent':
            ret.parent = to_json(localize_meta(v, ret.lang)) # do NOT stringify!
        elif k == 'title':
            ret.title = stringify(localize_meta(v, ret.lang))
        elif k == 'date':
            ret.date = stringify(localize_meta(v, ret.lang))
        elif k == 'summary':
            ret.summary = to_json(localize_meta(v, ret.lang)) # do NOT stringify!

    meta['lang'] = MetaString(ret.lang)
    meta['self'] = MetaString(stem) # no preceding /, provided from rootpath
    meta['base'] = MetaString(rawstem) # similar to self but without lang
    if git:
        meta['git'] = MetaMap(dict((k, MetaString(v)) for k, v in git.items()))

    if ret.short:
        ret.redirect_from.append(ret.short)

    for i in ret.redirect_from:
        assert not re.search(r'\.[a-z]{2}$', i.lower()), \
            'redirect-from entry %r contains a language component' % i

    def resolve_kwlink(beforepipe, inside):
        page = u' '.join(stringify(beforepipe or inside).split())
        if page:
            page, fragsep, frag = page.partition('#')
            word, querysep, query = page.partition('?')
            word = normalize_keyword(word)
            target = ('@' + urllib.quote(word.encode('utf-8')) +
                      querysep + urllib.quote(query.encode('utf-8')) +
                      fragsep + urllib.quote(frag.encode('utf-8')))
            ret.refs.add(KEYWORDS_PATH + word + u'.' + ret.lang)
            return Link(('', [], []), inside, (target, ''))
        else:
            out = [Str('[[')]
            if beforepipe is not None:
                out += beforepipe
                out.append(Str('|'))
            out += inside
            out.append(Str(']]'))
            return out

    def convert_kwlinks_from_inlines(inlines):
        outside = []
        inside = [None, None] # [beforepipe, inside]

        def rollback_inside():
            outside.append(Str('[[')) # reconstruct the opening token
            if inside[0] is not None:
                outside.extend(inside[0])
                outside.append(Str('|'))
            outside.extend(inside[1])
            inside[:] = None, None

        for i in inlines:
            # [[ and ]] tokens found in Str are checked
            if i['t'] == 'Str':
                text = i['c']

                if inside[1] is not None:
                    # find the possible ]] token first
                    sep = text.find('[')
                    sep2 = text.find(']')
                    if sep < 0 or sep > sep2: sep = sep2

                    pipe = text.find('|')
                    rollback = False
                    if pipe >= 0 and (sep < 0 or sep > pipe):
                        # [[link|label]] format: split the parts before | if appropriate
                        if inside[0] is None and inside[1]:
                            inside[:] = inside[1], []
                            if pipe > 0: inside[0].append(Str(text[:pipe]))
                            text = text[pipe+1:]
                            if sep >= 0: sep -= pipe + 1 # adjust sep for later ops
                        else:
                            rollback = True # duplicate pipes are invalid

                    if not rollback and sep < 0:
                        # no more separator found, continue adding to inside
                        inside[1].append(Str(text))
                        continue
                    elif not rollback and text[sep:sep+2] == ']]':
                        # the current keyword link is closed
                        if sep > 0: inside[1].append(Str(text[:sep]))
                        outside.append(resolve_kwlink(*inside))
                        inside[:] = None, None
                        text = text[sep+2:]
                    else:
                        # the possible keyword link contains non-matching separator
                        # it is an error, so bail out and rematch text below
                        rollback_inside()

                parts = re.split(r'\[\[([^\[\]]*)(\]\]|$)', text)
                assert len(parts) % 3 == 1 # (<text> <link> <closing>)* <text>
                if len(parts) > 1 and not parts[-2]:
                    assert not parts[-1]
                    beginning = parts[-3]
                    del parts[-3:]
                else:
                    beginning = None
                for i in xrange(0, len(parts)-1, 3):
                    if parts[i]: outside.append(Str(parts[i]))
                    # test if it has pipes: only [[a]], [[a|b]], [[a|]] are allowed
                    subparts = parts[i+1].split('|')
                    if len(subparts) == 1 and subparts[0]:
                        outside.append(resolve_kwlink(None, [Str(subparts[0])]))
                    elif len(subparts) == 2 and subparts[0]:
                        outside.append(resolve_kwlink([Str(subparts[0])], [Str(subparts[1])]))
                    else: # error
                        if parts[i+1]: outside.append(Str(parts[i+1]))
                    assert parts[i+2] == ']]'
                if parts[-1]: outside.append(Str(parts[-1]))
                if beginning is not None:
                    # this may also contain pipes
                    subparts = beginning.split('|')
                    if len(subparts) == 1:
                        inside[:] = None, []
                        if subparts[0]: inside[1].append(Str(subparts[0]))
                    elif len(subparts) == 2 and subparts[0]:
                        inside[:] = [Str(subparts[0])], []
                        if subparts[1]: inside[1].append(Str(subparts[1]))
                    else: # error
                        if beginning: outside.append(Str(beginning))

            # other inline parts are passed verbatim
            elif inside[1] is not None:
                # ...unless the element breaks the current line
                if i['t'] in ('SoftBreak', 'LineBreak'): rollback_inside()
                else: inside[1].append(i)
            else:
                outside.append(i)

        # if the inline still remains, the keyword link is invalid
        if inside[1] is not None: rollback_inside()

        return outside

    def inner(key, value):
        if key in ('Plain', 'Para', 'Emph', 'Strong', 'Strikeout',
                   'Superscript', 'Subscript', 'SmallCaps'):
            return {'t': key, 'c': convert_kwlinks_from_inlines(value)}
        elif key == 'Table':
            value[0] = convert_kwlinks_from_inlines(value[0])
            return {'t': key, 'c': value}
        elif key in ('Quoted', 'Cite', 'Span'): # note no Link and Image
            value[1] = convert_kwlinks_from_inlines(value[1])
            return {'t': key, 'c': value}
        elif key == 'Header':
            value[2] = convert_kwlinks_from_inlines(value[2])
            return {'t': key, 'c': value}
        elif key == 'DefinitionList':
            return DefinitionList([(convert_kwlinks_from_inlines(t), d) for t, d in value])

    doc = walk(doc, inner)

    # try to generate the summary if not available
    if ret.summary is None:
        assert len(doc) == 2
        collected = []
        cut = None
        more = False
        for i in doc[1]:
            collected.append(i)
            if i['t'] == 'RawBlock':
                fmt, html = i['c']
                if fmt == 'html' and ''.join(html.lower().split()) == '<!--more-->':
                    more = True
                    i['c'] = fmt, '<!-- more -->' # canonicalize comment
                    break
            elif i['t'] in ('Header', 'HorizontalRule'):
                if cut is None and collected: cut = len(collected) - 1
        if not more and cut:
            del collected[cut:]
            # simulate the `<!-- more -->` comment if none
            collected.append(RawBlock('html', '<!-- more -->'))
            doc[1].insert(cut, RawBlock('html', '<!-- more -->'))
        ret.summary = to_json(MetaBlocks(collected))

    return doc, ret

def get_available_langs(pat, rawstem):
    dirpath, pat = os.path.split(pat.replace('%', rawstem + '.%'))
    assert '%' not in dirpath
    prefix, sep, suffix = pat.partition('%')
    assert sep

    for f in os.listdir(dirpath):
        if f.startswith(prefix) and f.endswith(suffix):
            yield f[len(prefix):len(f)-len(suffix)]

def get_gitinfo(path):
    proc = subprocess.Popen(
        ['git', 'log', '-1', '--pretty=format:%H%x00%at%x00%s',
         'HEAD', '--', path],
        stdout=subprocess.PIPE)
    stdout = proc.communicate()[0].split('\0')
    if len(stdout) == 3:
        commit, lastmod, shortlog = stdout
        lastmod = int(lastmod)
        shortlog = shortlog.decode('utf-8', 'replace')
        return dict(
            rev = commit,
            shortrev = commit[:12],
            lastmod = time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime(lastmod)),
            lastmodutc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(lastmod)),
            shortlog = shortlog,
        )

SCHEMA_VERSION = 1
def update_to_indices(dbpath, ret):
    db = sqlite3.connect(dbpath)
    ver, = db.execute('pragma user_version').fetchone()
    assert ver == SCHEMA_VERSION, 'check-schema didn\'t really work; ver = %r' % ver
    rawstem = unicodedata.normalize('NFC', ret.rawstem.decode('utf-8'))
    lang = ret.lang.decode('utf-8')
    short = ret.short
    if not short and 1 <= len(rawstem) <= 4 and all(c.isalnum() or c in '._-' for c in rawstem):
        short = rawstem # the raw stem and short link is same, short itself is omitted to avoid cycles
    order = None
    if ret.template == 'journal':
        order = 'journal;%s;%s' % (ret.date or '', rawstem)
    db.execute('''
        insert or replace into
        pages(stem, lang, short, parent, title, date, "order", summary)
        values(?, ?, ?, ?, ?, ?, ?, ?);
    ''', (rawstem, lang, ret.short, ret.parent, ret.title, ret.date, order, ret.summary))
    db.executemany('''
        insert or replace into redirects(stem, lang, target) values(?, ?, ?);
    ''', [(i, lang, rawstem) for i in ret.redirect_from])
    db.commit()
    db.close()

def main(dbpath, inputpat, jsoninpat, jsonoutpat, auxpat, depspat, gendepspat, refspat, targetpat, targetrespat, path):
    # so that e.g. `path/to/%.foo` can be `replace`d with a needle `%`
    assert not path.endswith('/')

    stem = path.lstrip('/')
    path = '/' + stem
    input = inputpat.replace('%', stem)
    jsonin = jsoninpat.replace('%', stem)
    jsonout = jsonoutpat.replace('%', stem)
    deps = depspat.replace('%', stem)
    refs = refspat.replace('%', stem)
    target = targetpat.replace('%', stem)

    with open(jsonin, 'rb') as f:
        doc = json.load(f)

    doc, ret = transform(doc, stem=stem, git=get_gitinfo(input))

    # now search for other languages and put the list of them to the metadata
    langs = list(get_available_langs(inputpat, ret.rawstem))
    otherlangs = set(langs)
    otherlangs.discard(ret.lang)

    # a list of languageless "short" URLs to be redirected
    multistems = [ret.rawstem] + ret.redirect_from
    multideps = gendepspat.replace('%', ret.rawstem + '_multichoice')

    with open(jsonout, 'wb') as f:
        json.dump(doc, f, separators=(',', ':'))

    uniqid = hashlib.sha1(ret.rawstem).hexdigest()
    multijsonoutkey = 'MULTICHOICE_JSONOUT_' + uniqid
    availlangkey = 'AVAIL_LANGUAGES_' + uniqid

    with open(deps, 'wb') as f:
        print >>f, '$(eval $(call JSON_TO_HTML_RULE,%s,%s,%s,%s,%s,%s,%s,%s,%s))' % (jsonout, refs, target, path, ret.rawstem, ret.template + '.' + ret.lang, ret.lang, availlangkey, ' '.join(refspat.replace('%', i.encode('utf-8')) for i in ret.refs))
        for redir in ret.redirect_from:
            redir = (redir + '.' + ret.lang).encode('utf-8')
            print >>f, '$(eval $(call REDIRECT_RULE,%s,%s,%s,%s,%s))' % (jsonout, targetpat.replace('%', redir), '/' + redir, target, path)
        print >>f, '%s += %s' % (multijsonoutkey, jsonout)
        print >>f, '%s += %s' % (availlangkey, ret.lang)
        for respath in ret.resources:
            respath = posixpath.normpath(posixpath.join(posixpath.dirname(path), respath))
            # need to add both: TARGETS used for purging unused files, targets used for deps
            print >>f, 'TARGETS += %s' % targetrespat.replace('%', respath[1:])
            print >>f, 'targets: %s' % targetrespat.replace('%', respath[1:])

    # technically speaking this should spawn multiple dependency files,
    # but we cannot easily plug them into Makefile.
    # instead, we assume that the set of redirections in same pages
    # with differing languages is identical, so we can make use of
    # the "primary" dependency file which is readily known to Makefile.

    # update atomically, by creating a uniquely named temporary file and renaming this.
    with tempfile.NamedTemporaryFile(dir=os.path.dirname(multideps), delete=False) as f:
        multitarget = targetpat.replace('%', ret.rawstem)
        print >>f, '$(eval $(call MULTICHOICE_RULE,$(%s),%s,%s,%s))' % (multijsonoutkey, ' '.join(langs), multitarget, '/' + ret.rawstem)
        for redir in multistems[1:]:
            # ANY page in the cluster can be used for this purpose
            redir = redir.encode('utf-8')
            print >>f, '$(eval $(call REDIRECT_RULE,$(%s),%s,%s,%s,%s))' % (multijsonoutkey, targetpat.replace('%', redir), '/' + redir, targetpat.replace('%', ret.rawstem), '/' + ret.rawstem)

        # flushing the fsyncing is required: http://stackoverflow.com/q/7433057
        f.flush()
        os.fsync(f.fileno())

    # not really portable (Windows will fail on dups), but Python 2 doesn't have os.replace
    os.rename(f.name, multideps)

    # touch reference files if they do not exist
    for path in ret.refs:
        path = refspat.replace('%', path.encode('utf-8'))
        if not os.path.exists(path):
            # this needs not to be atomic
            try: os.makedirs(os.path.dirname(path))
            except Exception: pass
            with open(path, 'w'): pass

    update_to_indices(dbpath, ret)

if __name__ == '__main__':
    if len(sys.argv) < 11:
        print >>sys.stderr, 'Usage: %s <indices db> <input page pattern> <input json pattern> <output json pattern> <auxiliary file pattern> <dependency file output pattern> <generated dependency file output pattern> <references pattern> <target pattern> <target resource pattern> <path>' % sys.argv[0]
        raise SystemExit(1)

    _, dbpath, inputpat, jsoninpat, jsonoutpat, auxpat, depspat, gendepspat, refspat, targetpat, targetrespat, path = sys.argv[:12]
    main(dbpath, inputpat, jsoninpat, jsonoutpat, auxpat, depspat, gendepspat, refspat, targetpat, targetrespat, path)

