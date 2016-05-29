dnl a part of mearie.org, used in /pages/documents/index
dnl
$for(categories)$
<h2 id="$categories.id$">$categories.title$</h2>
<section class="mearie-entries">
$for(categories.entries)$
<section class="mearie-entry">
<h3>dnl
$if(categories.entries.link)$<a href="$categories.entries.link$">$endif$dnl
$categories.entries.title$dnl
$if(categories.entries.link)$</a>$endif$dnl
$if(categories.entries.date)$ ($categories.entries.date$)$endif$dnl
</h3>
$categories.entries.desc$
</section>
$endfor$
</section>
$endfor$
