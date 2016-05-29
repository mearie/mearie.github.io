# coding=utf-8
#
# a part of mearie.org

import sys
import re
import sqlite3
import unicodedata
from cgi import escape
from urllib import quote as urlquote, unquote as urlunquote
from urlparse import urlparse
from HTMLParser import HTMLParser


SCHEMA_VERSION = 1
def open_db(dbpath):
    db = sqlite3.connect(dbpath)
    ver, = db.execute('pragma user_version').fetchone()
    assert ver == SCHEMA_VERSION, 'check-schema didn\'t really work; ver = %r' % ver
    return db

UNSHORTEN_CACHE = {} # (stem, lang) -> target
def unshorten(db, stem, lang):
    try:
        return UNSHORTEN_CACHE[stem, lang]
    except KeyError:
        c = db.execute('''select target from redirects
                          where stem = ? and lang = ?''', (stem, lang))
        target, = c.fetchone() or (None,)
        if target:
            target += '.' + lang
        else:
            # use multilanguage page if the exact language is not available
            c = db.execute('''select target from redirects
                              where stem = ? limit 1''', (stem,))
            target, = c.fetchone() or (None,)
        UNSHORTEN_CACHE[stem, lang] = target
        return target

KEYWORDS_PATH = u'w/'
KEYWORDS_CACHE = {} # (word, lang) -> bool
def keyword_exists(db, word, lang):
    try:
        return KEYWORDS_CACHE[word, lang]
    except KeyError:
        c = db.execute('''select 1 from pages
                          where stem = ? and lang = ?''', (KEYWORDS_PATH + word, lang))
        exists = c.fetchone() is not None
        if not exists:
            c = db.execute('''select 1 from redirects
                              where stem = ? and lang = ?''', (KEYWORDS_PATH + word, lang))
            exists = c.fetchone() is not None
        KEYWORDS_CACHE[word, lang] = exists
        return exists


WP_NAME_PATTERN = re.compile(r'^([a-z-]+):(.*)$', re.I)
WP_FRAGMENT_PATTERN = re.compile(r'%([0-9a-f]{2})', re.I)
def resolve_wikipedia_url(parsed, preferred_lang):
    '''w:[<lang>:]<name> (with <fragment> specially handled)'''
    name = parsed.path + parsed.params
    m = WP_NAME_PATTERN.search(name)
    lang, local_name = (m.group(1), m.group(2)) if m else (preferred_lang, name)
    if not lang: return # no language information available
    local_name = urlquote('_'.join(local_name.replace('%20', ' ').split()))
    if parsed.fragment:
        fragment = WP_FRAGMENT_PATTERN.sub(r'.\1', urlquote('_'.join(parsed.fragment.split())))
    else:
        fragment = ''
    return 'https://{lang}.wikipedia.org/wiki/{name}{query}{fragment}'.format(
        lang=lang, name=local_name,
        query=('?' + parsed.query if parsed.query else ''),
        fragment=('#' + fragment if fragment else ''))

def resolve_namuwiki_url(parsed, preferred_lang):
    '''a:<name>'''
    return 'https://namu.wiki/w/{name}{query}{fragment}'.format(
        name=urlquote(parsed.path + parsed.params),
        query=('?' + parsed.query if parsed.query else ''),
        fragment=('#' + urlquote(parsed.fragment) if parsed.fragment else ''))

def resolve_github_url(parsed, preferred_lang):
    '''gh:<user> / gh:[<user>]/<repo> (<user> defaults to lifthrasiir)'''
    parts = (parsed.path + parsed.params).split('/')
    if len(parts) == 1:
        return 'https://github.com/{user}'.format(user=parts[0])
    elif len(parts) == 2:
        return 'https://github.com/{user}/{repo}'.format(
            user=parts[0] or 'lifthrasiir', repo=parts[1])
    else:
        return

def resolve_bitbucket_url(parsed, preferred_lang):
    '''bb:<user> / bb:[<user>]/<repo> (<user> defaults to lifthrasiir)'''
    parts = (parsed.path + parsed.params).split('/')
    if len(parts) == 1:
        return 'https://bitbucket.org/{user}'.format(user=parts[0])
    elif len(parts) == 2:
        return 'https://bitbucket.org/{user}/{repo}'.format(
            user=parts[0] or 'lifthrasiir', repo=parts[1])
    else:
        return

CUSTOM_RESOLVERS = dict(
    w = resolve_wikipedia_url,
    a = resolve_namuwiki_url,
    gh = resolve_github_url,
    bb = resolve_bitbucket_url,
)
def resolve_url(url, preferred_lang, db=None):
    # custom resolver
    # XXX urlparse doesn't handle custom scheme well depending on minor version (!)
    scheme, sep, hier = url.strip().partition(':')
    if sep:
        parsed = urlparse('http:' + hier) # we *know* that http: works fine
        assert parsed.scheme == 'http'
        parsed = parsed._replace(scheme=scheme)
    else:
        parsed = urlparse(scheme)
    try:
        ret = CUSTOM_RESOLVERS[parsed.scheme](parsed, preferred_lang)
        if ret: return ret
    except KeyError:
        pass

    # default resolver
    if preferred_lang:
        # a URL ending with a dot (.) is a placeholder for the correct lang tag.
        # customarily a short URL of the form /x thru /xxxx also gets the lang tag.
        path = parsed.path + parsed.params
        if not parsed.scheme and not parsed.hostname: # no absolute path
            path_changed = False
            if path.endswith('/.'): # foo/. == foo/index.<lang>
                path = path[:-1] + 'index.' + preferred_lang
                path_changed = True
            elif path.endswith('.'): # foo. == foo.<lang>
                path += preferred_lang
                path_changed = True
            elif path.startswith('/') and 1 <= len(path) <= 5 and \
                    all(c.isalnum() or c in '._-' for c in path[1:]): # /xxx == /xxx.<lang>
                if len(path) == 1:
                    path += 'index' + '.' + preferred_lang
                elif db:
                    # try to resolve the short URL if available
                    unshortened = unshorten(db, path[1:].decode('utf-8'), preferred_lang)
                    if unshortened: path = '/' + unshortened.encode('utf-8')
                else:
                    path += '.' + preferred_lang
                path_changed = True
            if path_changed:
                return '{path}{query}{fragment}'.format(
                    path=path,
                    query=('?' + parsed.query if parsed.query else ''),
                    fragment=('#' + parsed.fragment if parsed.fragment else ''))

    # fallback: no change to the URL
    return url

KEYWORD_SEP2DASH_PATTERN = re.compile(ur'(?<=[a-z])[^\w._]+|[^\w._]+(?=[a-z])|'
                                      ur'(?<=[a-z0-9])[^\w._]+(?=[a-z0-9])', re.U)
def normalize_keyword(word):
    word = unicodedata.normalize('NFC', word)
    word = u''.join(c if c.isalnum() or c in '._' else u' ' for c in word.lower())
    word = u''.join(KEYWORD_SEP2DASH_PATTERN.sub(u'-', word).split()).strip(u'-')
    return word

if True: # sanity tests
    def test_eq(actual, expected):
        if actual == expected: return
        print >>sys.stderr, '*** sanity test failed: %r expected, %r actual' % (expected, actual)
        raise SystemExit(2)

    test_eq(resolve_url('w:뷁', 'ko'), 'https://ko.wikipedia.org/wiki/%EB%B7%81')
    test_eq(resolve_url('w:What the fuck#See also', 'en'),
            'https://en.wikipedia.org/wiki/What_the_fuck#See_also')
    test_eq(resolve_url('w:What%20the%20fuck#See also', 'en'),
            'https://en.wikipedia.org/wiki/What_the_fuck#See_also')
    test_eq(resolve_url('w:ja:くそ?redirect=no', 'en'),
            'https://ja.wikipedia.org/wiki/%E3%81%8F%E3%81%9D?redirect=no')
    test_eq(resolve_url('w:ko:백과사전#같이 읽기', 'en'),
            'https://ko.wikipedia.org/wiki/%EB%B0%B1%EA%B3%BC%EC%82%AC%EC%A0%84'
            '#.EA.B0.99.EC.9D.B4_.EC.9D.BD.EA.B8.B0')
    test_eq(resolve_url('a:백과사전', 'en'),
            'https://namu.wiki/w/%EB%B0%B1%EA%B3%BC%EC%82%AC%EC%A0%84')
    test_eq(resolve_url('a:백과사전#s-1.1', 'en'),
            'https://namu.wiki/w/%EB%B0%B1%EA%B3%BC%EC%82%AC%EC%A0%84#s-1.1')
    test_eq(resolve_url('http://mearie.org/', 'en'), 'http://mearie.org/')
    test_eq(resolve_url('http://mearie.org/heck', 'en'), 'http://mearie.org/heck')
    test_eq(resolve_url('/heck', 'ko'), '/heck.ko')
    test_eq(resolve_url('/heck?a=b#c', 'ko'), '/heck.ko?a=b#c')
    test_eq(resolve_url('/heck.', 'ko'), '/heck.ko')
    test_eq(resolve_url('/heck.en', 'ko'), '/heck.en')
    test_eq(resolve_url('/heck.en?a=b#c', 'ko'), '/heck.en?a=b#c')
    test_eq(resolve_url('/heck.html', 'ko'), '/heck.html')
    test_eq(resolve_url('/what-the-heck', 'ko'), '/what-the-heck')
    test_eq(resolve_url('/what-the-heck.', 'ko'), '/what-the-heck.ko')
    test_eq(resolve_url('/what-the-heck.en', 'ko'), '/what-the-heck.en')
    test_eq(resolve_url('/a/#foo', 'ko'), '/a/#foo')
    test_eq(resolve_url('/a/.#foo', 'ko'), '/a/index.ko#foo')
    test_eq(resolve_url('/a/./#foo', 'ko'), '/a/./#foo')
    test_eq(resolve_url('/#foo', 'ko'), '/index.ko#foo')
    test_eq(resolve_url('/.#foo', 'ko'), '/index.ko#foo')
    test_eq(resolve_url('/./#foo', 'ko'), '/./#foo')
    test_eq(resolve_url('#foo', 'ko'), '#foo')


URL_ATTRIBUTES = {
    'cite': ('blockquote', 'del', 'ins', 'q'),
    'data': ('object',),
    'href': ('a', 'area'), # link and base should not be resolved
    'icon': ('menuitem',),
    'poster': ('video',),
    'src': ('audio', 'embed', 'iframe', 'img', 'input', 'script', 'source', 'track', 'video'),
}

class FilteringHTMLParser(HTMLParser):
    def __init__(self, out, db):
        HTMLParser.__init__(self)
        self.out = out
        self.db = db
        self.preferred_lang = None
        self.header_selflink = None # or ('tag', 'id')

    def _update_attr(self, attrs, newk, newv):
        for i, (k, _) in enumerate(attrs):
            if k == newk:
                if newv: attrs[i] = k, newv
                else: del attrs[i]
                return attrs
        if newv: attrs.append((newk, newv))
        return attrs

    def _add_class(self, attrs, newcls):
        newattrs = []
        clsadded = False
        for k, v in attrs:
            if not clsadded and k == 'class':
                newattrs.append((k, v + ' ' + newcls if v else v))
                clsadded = True
            else:
                newattrs.append((k, v))
        if not clsadded:
            newattrs.append(('class', newcls))
        return newattrs

    def _format_starttag(self, tag, attrs):
        ret = [tag]
        for k, v in attrs:
            if v is None:
                ret.append(' {}'.format(k))
            else:
                if tag in URL_ATTRIBUTES.get(k, ()):
                    v = resolve_url(v, self.preferred_lang, db=self.db)
                ret.append(' {}="{}"'.format(k, escape(v)))
        return ''.join(ret)

    def handle_starttag(self, tag, attrs):
        attrsdict = dict(attrs)
        if tag == 'html': self.preferred_lang = attrsdict.get('lang')

        if not self.header_selflink and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and \
                                        attrsdict.get('id'):
            # should append the link at the end, so we wait until next handle_endtag
            self.header_selflink = (tag, attrsdict['id'])
            attrs = self._add_class(attrs, 'header-has-selflink')

        elif tag == 'a' and attrsdict.get('href', '').lstrip().startswith('@'):
            # keyword links: src=@ABC maps to src=/w/ABC.<lang> or class=dead
            word = attrsdict['href'].lstrip()[1:]
            word, fragsep, frag = word.partition('#')
            word, querysep, query = word.partition('?')
            word = urlunquote(word).decode('utf-8')
            word = normalize_keyword(word)
            href = '/' + KEYWORDS_PATH.encode() + urlquote(word.encode('utf-8')) + '.' + self.preferred_lang + querysep + query + fragsep + frag
            attrs = self._update_attr(attrs, 'title', (u'→ ' + word).encode('utf-8'))
            if keyword_exists(self.db, word, self.preferred_lang):
                attrs = self._update_attr(attrs, 'href', href)
                attrs = self._add_class(attrs, 'keyword')
            else:
                attrs = self._update_attr(attrs, 'href', None)
                attrs = self._update_attr(attrs, 'data-dead-href', href)
                attrs = self._add_class(attrs, 'keyword dead')

        self.out.write('<{}>'.format(self._format_starttag(tag, attrs)))

    def handle_endtag(self, tag):
        if self.header_selflink and self.header_selflink[0] == tag:
            self.out.write(' <a href="#{id}" class="header-selflink">#</a>'.format(id=self.header_selflink[1]))
            self.header_selflink = None
        self.out.write('</{}>'.format(tag))

    def handle_startendtag(self, tag, attrs):
        self.out.write('<{} />'.format(self._format_starttag(tag, attrs)))

    def handle_data(self, data):
        self.out.write(data)

    def handle_entityref(self, name):
        self.out.write('&{};'.format(name))

    def handle_charref(self, name):
        self.out.write('&#{};'.format(name))

    def handle_comment(self, data):
        self.out.write('<!--{}-->'.format(data))

    def handle_decl(self, decl):
        self.out.write('<!{}>'.format(decl))

    def handle_pi(self, data):
        self.out.write('<?{}>'.format(data))

    def close(self):
        HTMLParser.close(self)
        return self.out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, 'Usage: %s <indices db> < <input html> > <output html>' % sys.argv[0]
        raise SystemExit(1)

    db = open_db(sys.argv[1])
    parser = FilteringHTMLParser(sys.stdout, db)
    parser.feed(sys.stdin.read())
    parser.close()

