// a part of mearie.org

;(function() {
	"use strict";

	// pre-IE8 styling hack
	if (/*@cc_on!@*/false && document.getElementById && document.createElement) {
		var newElems = 'abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output progress section summary template time video'.split(/ /);
		for (var i = newElems.length; i-- > 0; ) document.createElement(newElems[i]);
		window.onload = function() { // ...and put a PNG replacement to SVG
			var logo = document.getElementById('mearie-logo');
			if (!logo) return;
			logo.innerHTML = logo.innerHTML.replace(/<\/svg>/i,
				'<image xlink:href="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA' +
				'AQAAAAEABAMAAACuXLVVAAAAElBMVEVHcEx2VYh1VYl2VIh2VIh3VYggL1ZZAAAABXRSTlMA' +
				'HT9txAN1OB0AAAIvSURBVHja7dpPU4MwEIfhpdU7juMdR73Tqnc6lXuB8P2/iiflT6BFifmN' +
				'0zdnkj4zSZZlu2Yv7YJRmZmZPYR+tjYDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' +
				'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgNAA93FQAo6P' +
				'9jUUgGNqthLQvE6PfMmiO7N5wPS6uzHgZGfHWUB+7lk3v2goQG5awMG0gNq0AJeKAblpAY2J' +
				'AbkY0JgYkIsBjYkBhRqQigG1iQGFGjDegXQScDc50gCA4R3YvK1LSn8BGEy5L9tQgGTfH2dS' +
				'sn4U2q5Oy0/DtZYkpb3fT0oBoPHOc2RAZeMpkQGFd6EjA7ozuGklgC4M3WgA3Q68SwBdjE9a' +
				'CaDxJ1RhXkYLAd27+FYDqPx14gJO3hmMDOjiUKkGtNcOSK4ewBnQX8PySiOh/GVUewlRZEDj' +
				'pYSXANuFteIfZ0Tfp/AC4PbPktIHDSDzZkQGFN4eRAb0Ps1uJID+x2mpALhxeSAUYPPRH8X8' +
				'x0bWEzwHBCwu0QyKZG8CwLBM+FRGB4yifPK0CxOKl9cJc3WhslIDnBowswcRAbUaMIhFEkCl' +
				'BrhU/b9hrQZMnYK4gEYN8NsHojcwZGqAdxOi95CMBdEBrcsCAFY1MrndYuxsRrQKMOjkUjWz' +
				'ueM+o58QAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wvwCQW4x20xXleUAAAAAElFTkSuQmCC" ' +
				'width="100%" height="100%" border="0" /></svg>');
		};
	}

	// never run JS on very old browsers, the entire website works without JS anyway
	if (!document.querySelector || !document.querySelectorAll) return;

	// various polyfills
	function $(s, e) { return (e || document).querySelector(s); };
	function $$(s, e) { return (e || document).querySelectorAll(s); };
	function $each(a, f) { for (var i = 0, n = a.length; i < n; ++i) f(a[i]); };
	var $on;
	if (window.addEventListener) {
		$on = function(e, name, f) { e.addEventListener(name, f); }
	} else {
		$on = function(e, name, f) { e.attachEvent('on' + name, function() { f.call(e); }); }
	}
	function $has(e, cls) {
		var clss = (e.className || '').split(/\s+/);
		for (var i = 0, n = clss.length; i < n; ++i) {
			if (clss[i] == cls) return true;
		}
		return false;
	}
	function $set(e, cls) {
		if (!$has(e, cls)) e.className = (e.className ? e.className + ' ' + cls : cls);
	}
	function $unset(e, cls) {
		var clss = (e.className || '').split(/\s+/);
		for (var i = 0, n = clss.length; i < n; ++i) {
			if (clss[i] == cls) {
				var last = clss.pop();
				if (i < n - 1) clss[i] = last;
				e.className = clss.join(' ');
				return;
			}
		}
	}
	if (!Event.prototype.preventDefault) {
		Event.prototype.preventDefault = function() { this.returnValue = false; };
	}
	if (!Event.prototype.stopPropagation) {
		Event.prototype.stopPropagation = function() { this.cancelBubble = true; };
	}
	window.requestAnimationFrame = window.requestAnimationFrame ||
		window.msRequestAnimationFrame || window.mozRequestAnimationFrame ||
		window.webkitRequestAnimationFrame || window.oRequestAnimationFrame;
	if (!window.requestAnimationFrame) { // simulate rAF with fixed 60 Hz frame rate
		var rafTimer = null, rafPending = [];
		window.requestAnimationFrame = function(f) {
			if (rafTimer === null) {
				rafTimer = setTimeout(function() {
					for (var i = 0, n = rafPending.length; i < n; ++i) rafPending[i]();
					rafPending = [];
					rafTimer = null;
				}, 16);
			}
			rafPending.push(f);
		};
	}

	function alterAddressBar() {
		if (!history.replaceState) return;

		// check if the specific page was chosen by the referrer.
		// also, even when it doesn't seem so, if the referrer has a lang info,
		// it means that the referrer's referrer (if any) wants this specific page.
		var referrer = document.referrer || '';
		var origin = location.origin || (location.protocol + '//' + location.host);
		if (referrer.substring(0, origin.length) !== origin) return;
		if (referrer.match(/\.[a-z]{2}(?:\.html)?$/i)) return;

		var canonical = $('link[rel=canonical]');
		var shortlink = $('link[rel=shortlink]');

		// canonical has a lang info, shortlink doesn't
		if (canonical && canonical.href && canonical.href.match(/\.[a-z]{2}$/i)) {
			var href = canonical.href.replace(/(?:(\/)index)?\.[a-z]{2}$/i, '$1');
			history.replaceState(history.state, '', href + location.hash);
		}
	}
	alterAddressBar();
	$on(window, 'popstate', alterAddressBar);

	function onFootnoteClick(e) {
		e = e || event;

		var href = this.getAttribute('href') || '';
		if (!href.match(/^#/)) return;
		var target = document.all[href.substring(1)];
		if (!target) return;

		e.stopPropagation();
		e.preventDefault();

		// remove the previous tooltip unless it is going to be identical
		var prevTooltip = $('#mearie-tooltip');
		var shouldShow = true;
		if (prevTooltip) {
			if (prevTooltip.previousSibling == this) shouldShow = false;
			prevTooltip.parentNode.removeChild(prevTooltip);
		}

		if (shouldShow) {
			var tooltip = document.createElement('aside');
			tooltip.setAttribute('id', 'mearie-tooltip');
			var tooltipInner = document.createElement('div');
			$each(target.childNodes, function(e) {
				tooltipInner.appendChild(e.cloneNode(true));
			});
			$on(tooltipInner, 'click', function(e) { (e || event).stopPropagation(); });
			tooltip.appendChild(tooltipInner);
			this.parentNode.insertBefore(tooltip, this.nextSibling);
		}
	}

	function applyKaTeX(math) {
		var css = document.createElement('link');
		css.setAttribute('rel', 'stylesheet');
		css.setAttribute('href', '//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.5.1/katex.min.css');
		document.body.appendChild(css);

		var script = document.createElement('script');
		script.setAttribute('src', '//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.5.1/katex.min.js');
		$on(script, 'load', function() {
			$each(math, function(e) {
				var span = document.createElement('span');
				katex.render(e.textContent, span, {
					displayMode: $has(e, 'math-display'),
					throwOnError: false
				});
				e.parentNode.replaceChild(span, e);
			});
		});
		document.body.appendChild(script);
	}

	function buildNav() {
		var home = $('#mearie-logo>a[rel=home]');
		if (!home || !home.href || home.href.match(/["<>&]/)) return;
		var root = home.href.split(/(?:\/|^)index/);
		if (root.length != 2) return;
		var prefix = root[0];
		var suffix = root[1];

		var menus, searchPlaceholder, searchSubmit, experimental;
		if (suffix === '.ko') {
			menus = [
				{url: '/about/index', title: '대하여'},
				{url: '/p/index', title: '소프트웨어'},
				{url: '/t/index', title: '글'},
				{url: '/w/index', title: '낱말'},
				{url: '/sitemap', title: '사이트맵'}
			];
			searchPlaceholder = '검색';
			searchSubmit = '구글 검색';
			experimental = '<a href="//mearie.org">메아리</a>의 새 버전을 테스트하는 중입니다. <span class="long">여기 있는 내용은 언제든지 사라질 수 있습니다.</span>';
		} else {
			menus = [
				{url: '/about/index', title: 'About'},
				{url: '/p/index', title: 'Software'},
				{url: '/t/index', title: 'Text'},
				//{url: '/w/index', title: 'Keywords'}, // really ko only
				{url: '/sitemap', title: 'Sitemap'}
			];
			searchPlaceholder = 'Search';
			searchSubmit = 'Google Search';
			experimental = 'We are testing a new version of <a href="//mearie.org">mearie.org</a>. <span class="long">Any content may go away without notice.</span>';
		}

		var nav = document.createElement('nav');
		var items = '';
		$each(menus, function(e) {
			items += '<li><a href="' + prefix + e.url + suffix + '">' + e.title + '</a></li>';
		});
		nav.innerHTML =
			'<p class="warning">' + experimental + '</p>' +
			'<ul>' +
				items +
			'</ul>' +
			'<form action="http://www.google.com/cse" class="search">' +
				'<input type="hidden" name="cx" value="017879559261112115196:ygyuirvfnku"/>' +
				'<input type="search" name="q" size="20" placeholder="' + searchPlaceholder + '"/>' +
				'<input type="submit" name="sa" value="' + searchSubmit + '"/>' +
			'</form>';
		document.body.insertBefore(nav, $('body>footer'));
		$set(document.body, 'mearie-nav-present');
	}

	var scrollTicked = false;
	var p = 0;
	function onScroll(logo) {
		if (scrollTicked) return;
		scrollTicked = true;
		window.requestAnimationFrame(function() {
			// we need to calculate the threshold on the fly, due to reflow
			var scroll = window.scrollY;
			if (typeof scroll === 'undefined') scroll = scroll.pageYOffset;
			if (typeof scroll === 'undefined') {
				if (!document.documentElement) return;
				scroll = document.documentElement.scrollTop;
			}
			var scrolled = (scroll >= logo.clientHeight);
			(scrolled ? $set : $unset)(document.body, 'mearie-scrolled');
			scrollTicked = false;
		});
	}

	function onDOMReady() {
		// build a navigation bar
		buildNav();

		// one-time scroll initialization
		if ($has(document.body, 'mearie-nav-present')) {
			var logo = $('#mearie-logo');
			if (logo) {
				onScroll(logo);
				$on(window, 'scroll', function() { onScroll(logo); });
				$on(document.body, 'touchstart', function() {});
				$on(document.body, 'touchmove', function() { onScroll(logo); });
			}
		}

		// footnote preparation
		$on($('html'), 'click', function() {
			var prevTooltip = $('#mearie-tooltip');
			if (prevTooltip) prevTooltip.parentNode.removeChild(prevTooltip);
		});
		$each($$('.footnote'), function(e) {
			$on(e, 'click', onFootnoteClick);
		});

		// math initialization
		var math = $$('.math');
		if (math.length > 0) applyKaTeX(math);
	}

	if (document.addEventListener) {
		document.addEventListener('DOMContentLoaded', onDOMReady);
	} else { // IE8 compatibility
		document.attachEvent('onreadystatechange', function() {
			if (document.readyState === 'complete') onDOMReady();
		});
	}
})()
