dnl a part of mearie.org, used in /pages/sitemap
dnl
<section id="mearie-sitemap">
<table>
<tbody>
$for(pages)$
<tr>
<th><a href="$rootpath$$pages.short$"><code>/$pages.short$</code></a></th>
<td>$if(pages.parent)$<small>$pages.parent$:</small> $endif$$pages.title$$if(pages.date)$ <time>$pages.date$</time>$endif$</td>
</tr>
$endfor$
</tbody>
</table>
</section>
