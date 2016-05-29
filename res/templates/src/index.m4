dnl a part of mearie.org, used in the index page
dnl
$for(recent)$
<article>
<h1>dnl
<span class="parent">dnl
$if(recent.parent)$$recent.parent$<span class="parentsep"> / </span>$endif$dnl
<span class="date"><a href="$rootpath$$recent.short$"><time>$recent.date$</time></a><br /></span>dnl
</span>dnl
$recent.title$dnl
</h1>
$recent.summary$
$if(recent.more)$<nav class="more"><a href="$rootpath$$recent.short$#$recent.more$">dnl
ifelse(LANG(),ko,`더 읽기',`Continue reading…')dnl
</a></nav>$endif$dnl
</article>
$endfor$
$tail$
