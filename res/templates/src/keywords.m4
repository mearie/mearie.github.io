dnl a part of mearie.org, used in /pages/keywords/index.ko
dnl
<section id="mearie-keywords">
$for(groups)$
<h2>$groups.name$</h2>
<ul>
$for(groups.words)$
<li><a href="$rootpath$$groups.words.url$" class="keyword">$groups.words.title$</a></li>
$endfor$
</ul>
$endfor$
</section>
