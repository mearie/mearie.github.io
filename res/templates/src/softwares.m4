dnl a part of mearie.org, used in /pages/projects/index
dnl
$for(categories)$
<h2 id="$categories.id$">$categories.title$</h2>
$categories.desc$
<section class="mearie-entries">
$for(categories.entries)$
<section class="mearie-entry">
<h3>dnl
$if(categories.entries.link)$<a href="$categories.entries.link$">$endif$dnl
$categories.entries.title$dnl
$if(categories.entries.link)$</a>$endif$dnl
$if(categories.entries.latest)$ <small>$categories.entries.latest$</small>$endif$dnl
</h3>
<div class="mearie-entrymeta">
$if(categories.entries.when)$dnl
<time>$categories.entries.when$</time>dnl
$else$dnl
ifelse(LANG(),ko,`dnl
<time>$categories.entries.since$</time>부터$if(categories.entries.until)$ <time>$categories.entries.until$</time>까지$endif$dnl
',`dnl
<time>$categories.entries.since$</time>–$if(categories.entries.until)$<time>$categories.entries.until$</time>$endif$dnl
')dnl
$endif$dnl
$if(categories.entries.license)$ | $categories.entries.license$$endif$dnl
$if(categories.entries.using)$ | $categories.entries.using$$endif$
</div>
$categories.entries.desc$
</section>
$endfor$
</section>
$endfor$
