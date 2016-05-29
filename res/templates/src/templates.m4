divert(-1)

# input variables (`LANG' mandatory, all others optional):
# `LANG' for the message language used in the templates
# `BODYCLASS' for the class of `body' element
# `PAGE' for special-purpose pages
# `BEFORE' for a name of the template file without `.m4' that goes before the main
# `AFTER' for a name of the template file without `.m4' that goes after the main
# `HIDETITLE' for hiding the generated title

define(`MEARIE_LOGO', `
<svg version="1.0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 182 186"ifelse($1,,,` $1')>
<path d="M0 0h54v102h-35v52h35v32h-54m34-70h20v24h-20" />
<path d="M64 0h54v100a22 22 0 0 0 0 56v30h-54m54-72a12 12 0 0 0 0 28v-28" />
<path d="M128 0h54v102h-33v12h33v8h-33v32h33v32h-54m35-52h19v8h-19" />
</svg>
')

# translated strings
ifelse(LANG(),ko,`
    define(`MEARIE_SITENAME', `메아리')
    define(`MEARIE_UNTITLED', `제목 없는 글')
    define(`MEARIE_OTHERLANGS', `다른 언어들')
    define(`MEARIE_LASTMOD', `마지막 수정 $1`'')
    define(`MEARIE_NOVERINFO', `버전 정보 없음')
    define(`MEARIE_COPYRIGHT', `저작권자 &copy; $1&ndash;$2, 강 성훈.')
    define(`MEARIE_SOMERIGHTS', `저작권을 약간 가집니다.')
    define(`MEARIE_MULTICHOICE', `다중 선택')
    define(`MEARIE_REDIRECTING', `이동 중...')
    define(`MEARIE_NOTFOUND', `문서 없음')
    define(`MEARIE_REDIRECTNOW', `아니면 바로 $1`'로 이동합니다.')
',LANG(),en,`
    define(`MEARIE_SITENAME', `mearie.org')
    define(`MEARIE_UNTITLED', `Untitled')
    define(`MEARIE_OTHERLANGS', `Other languages')
    define(`MEARIE_LASTMOD', `Last modified $1`'')
    define(`MEARIE_NOVERINFO', `No version information')
    define(`MEARIE_COPYRIGHT', `Copyright &copy; $1&ndash;$2, Kang Seonghoon.')
    define(`MEARIE_SOMERIGHTS', `Some rights reserved.')
    define(`MEARIE_MULTICHOICE', `Multiple Choices')
    define(`MEARIE_REDIRECTING', `Redirecting...')
    define(`MEARIE_NOTFOUND', `Not Found')
    define(`MEARIE_REDIRECTNOW', `Or jump directly to $1.')
',`
    errprint(`invalid `LANG' variable: 'ifdef(`LANG',`LANG')`
')
    m4exit(1)
')

# special-purpose pages
ifelse(PAGE(),multichoice,`

    # multiple choices
    # given a list of `$available_lang$', list pages out of the languages
    # and (in script) go to the most appropriate page from the browser settings
    define(`MEARIE_SPECIALPAGE')
    define(`MEARIE_SPECIALTITLE', `MEARIE_MULTICHOICE()')
    define(`MEARIE_SPECIALHEAD', `
<script>
var preferred = (navigator.userLanguage || navigator.language || "en").toLowerCase();
var langs = [$for(available_lang)$"$available_lang$",$endfor$`'0], hasen = false, chosen = "en";
for (var i = 0; langs[i]; ++i) {
	if (preferred.substring(0, langs[i].length) == langs[i]) { chosen = langs[i]; break; }
	hasen |= langs[i] == "en";
}
if (!hasen) chosen = langs[0];
location.replace("$rootpath$$self$." + chosen + location.hash);
</script>
')
    define(`MEARIE_SPECIALBODY', `
<ul>
$for(available_lang)$
<li><a href="$rootpath$$self$.$available_lang$" hreflang="$available_lang$">$self$.$available_lang$</a></li>
$endfor$
</ul>
')

',PAGE(),redirect,`

    # simple redirect to `$self$'
    define(`MEARIE_SPECIALPAGE')
    define(`MEARIE_SPECIALTITLE', `MEARIE_REDIRECTING()')
    define(`MEARIE_SPECIALHEAD', `
<script>
var referrer = document.referrer || "";
var origin = location.origin || (location.protocol + "//" + location.host);
if (referrer.substring(0, origin.length) === origin && !referrer.match(/\.[a-z]{2}(?:\.html)?$$/i)) {
	var href = location.href.replace(/(?:(\/)index)?\.[a-z]{2}$$/i, "`$$'1");
	history.replaceState(history.state, "", href + location.hash);
}
location.replace("$rootpath$$self$" + location.hash);
</script>
<meta http-equiv="Refresh" content="0; URL=$rootpath$$self$" />
')
    define(`MEARIE_SPECIALBODY', `
<p>MEARIE_REDIRECTNOW(`<a href="$rootpath$$self$">$self$</a>')</p>
')

',PAGE(),notfound,`

    # 404 not found
    define(`MEARIE_SPECIALPAGE')
    define(`MEARIE_SPECIALTITLE', `MEARIE_NOTFOUND()')
    define(`MEARIE_SPECIALHEAD', `')
    define(`MEARIE_SPECIALBODY', `')

')

# useful things
define(`LOCALIZED', `$if($1.LANG())$$$1.LANG()$$else$$$1$$endif$')

# disable comments from now on and switch to the templating mode
changecom()divert(0)dnl
<!doctype html>
ifdef(`MEARIE_SPECIALPAGE',`',`<!--[if gt IE 8]>-->')dnl
<html lang="$if(lang)$$lang$$else$LANG()$endif$">dnl
ifdef(`MEARIE_SPECIALPAGE',`',`<!--<![endif]--><!--[if lte IE 8]><html lang="$if(lang)$$lang$$else$LANG()$endif$" class="mearie-ancient"><![endif]-->')
<head>
<meta charset="utf-8">
ifdef(`MEARIE_SPECIALPAGE',`dnl
dnl
dnl special pages
dnl
<title>MEARIE_SPECIALTITLE() | MEARIE_SITENAME()</title>
MEARIE_SPECIALHEAD()dnl
<link rel="shortcut icon" href="$rootpath$favicon.ico" type="image/vnd.microsoft.icon" />
<style>body{background:#758}*{color:white}</style>
</head>
<body>dnl
MEARIE_LOGO(`width="182" height="186" fill="#fff"')dnl
<h1>MEARIE_SPECIALTITLE()</h1>dnl
MEARIE_SPECIALBODY()dnl
<address><a href="$rootpath$" rel="home">MEARIE_SITENAME()</a></address>
',`dnl
dnl
dnl ordinary pages with `$body$'
dnl
dnl `pagetitle' is for the ordinary HTML writer which is pre-escaped,
dnl `title' is for the default metadata which is parsed as a Markdown and rendered as HTML.
<title>$if(pagetitle)$$pagetitle$ | $else$$if(title)$LOCALIZED(title) | $endif$$endif$MEARIE_SITENAME()</title>
$for(author-meta)$
<meta name="author" content="$author-meta$" />
$endfor$
$if(date-meta)$
<meta name="date" content="$date-meta$" />
$endif$
<meta name="viewport" content="initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<link rel="canonical" href="$rootpath$$self$" />
<link rel="shortlink" href="$rootpath$$short$" />
<link rel="shortcut icon" href="$rootpath$favicon.ico" type="image/vnd.microsoft.icon" />
<!--[if gt IE 6]><![IGNORE[--><![IGNORE[]]>
<script src="$rootpath$res/mearie.js"></script>
<link rel="stylesheet" href="$rootpath$res/main.css" />
$for(css)$
<link rel="stylesheet" href="$css$" />
$endfor$
<!--<![endif]-->
</head>
<body`'ifdef(`BODYCLASS',` class="BODYCLASS()"')>
<header>
<div id="mearie-logo">
<a href="$rootpath$" rel="home">MEARIE_LOGO() MEARIE_SITENAME()</a>
</div>
ifdef(`HIDETITLE',`',`dnl
$if(title)$
<h1>dnl
$if(parent)$dnl
<span class="parent">LOCALIZED(parent)$if(date)$ / <time>$date$</time>$endif$<br /></span>dnl
$else$dnl
$if(date)$dnl
<span class="parent"><time>$date$</time><br /></span>dnl
$endif$dnl
$endif$dnl
LOCALIZED(title)$if(subtitle)$<br /><small>LOCALIZED(subtitle)</small>$endif$dnl
</h1>
$else$dnl
$if(parent)$dnl
<h1>dnl
<span class="parent">LOCALIZED(parent)$if(date)$ / <time>$date$</time>$endif$<br /></span>dnl
<em>MEARIE_UNTITLED()</em>dnl
</h1>
$else$dnl
$if(date)$dnl
<h1>dnl
<span class="parent"><time>$date$</time><br /></span>dnl
<em>MEARIE_UNTITLED()</em>dnl
</h1>
$endif$dnl
$endif$dnl
$endif$
')dnl
</header>
$if(toc)$
<div id="$idprefix$TOC" class="toc">
$toc$
</div>
$endif$
<main role="main">
ifdef(`BEFORE',`include(src/BEFORE.m4)')dnl
$body$
ifdef(`AFTER',`include(src/AFTER.m4)')dnl
</main>
<footer>
<p id="mearie-meta">dnl
<code><i class="mearie-logo"></i>$if(short)$/$short$$endif$</code>dnl
$if(otherlangs)$ | MEARIE_OTHERLANGS():$for(otherlangs)$ <a href="$rootpath$$base$.$otherlangs$" hreflang="$otherlangs$">$otherlangs$</a>$endfor$$endif$ | dnl
$if(git)$MEARIE_LASTMOD(`<time>$git.lastmod$</time> (<code>$git.shortrev$</code>)')$else$MEARIE_NOVERINFO()$endif$dnl
</p>
<address>MEARIE_COPYRIGHT(1999,2016) <a href="$rootpath$copy" rel="copyright">MEARIE_SOMERIGHTS()</a></address>
</footer>
')dnl
</body>
</html>
