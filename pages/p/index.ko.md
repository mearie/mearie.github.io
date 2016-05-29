---
title: 소프트웨어들
short: p
...

여기는 [강 성훈](/kang)이 만든 다양한 소프트웨어들을 모아 놓는 곳입니다.
기본적으로 아래 소프트웨어들의 소스 코드는 모두 공개되어 있으며,
만든이에게 책임을 지우지 않는 한 마음껏 쓸 수 있습니다.

---
template: softwares
categories:

- id: maintained
  title: 관리 중
  desc: |
	계속 갱신을 할 용의가 있거나 실제로 갱신을 하는 것들.
  entries:

	- title: 앙골모아
	  link: /angl
	  since: 2013
	  until: 2015
	  latest: 2.0 alpha 3
	  using: C, Rust, [SDL](https://libsdl.org/)
	  license: GPLv2+
	  desc: |
		최소주의 멀티플랫폼 리듬게임 비스무리한 무언가

	- title: Chrono
	  link: /chro
	  since: 2014-03
	  latest: 0.2.16
	  using: Rust
	  license: MIT + MPL + Apache
	  desc: |
		[Rust](https://rust-lang.org/)를 위한 날짜/시간 라이브러리

	- title: <abbr title="Cursive Script Object Notation">CSON</abbr>
	  link: /cson
	  since: 2013-02
	  desc: |
		[JSON](w:JSON)을 확장하여 손으로 쓰기 편하게 만든 직렬화 포맷

	- title: Encoding
	  link: /enco
	  since: 2013-07
	  latest: 0.2.32
	  using: Rust
	  license: MIT + MPL + Apache
	  desc: |
		[Rust](https://rust-lang.org/)를 위한 문자 인코딩 라이브러리

	- title: Unison
	  link: /unis
	  since: 2015-11
	  desc: |
		유니코드 전체를 커버하고 싶은 비트맵-윤곽선 복합 글꼴.

	- title: Sonorous
	  link: /snrs
	  since: 2013-02
	  until: 2014-12
	  using: Rust
	  license: GPLv2+
	  desc: |
		멀티플랫폼 리듬게임

- id: unmaintained
  title: 방치 중
  desc: |
	지속적으로 갱신할 필요가 없거나, 관심이 멀어졌거나 바빠서 못 건드는 것들.
	요청이 있고 시간이 있으면 갱신할 수도 있습니다.
  entries:

	- title: 아희아희
	  link: /ahah
	  when: 2015-04
	  using: 아희
	  license: CC0
	  desc: |
		[아희](https://aheui.github.io/)로 만든 아희 인터프리터

	- title: Esotope
	  link: /esot
	  since: 2009-05
	  until: 2012-05
	  using: Ocaml
	  desc: |
		난해한 프로그래밍 언어 구현체

	- title: hangeul.vim
	  link: /hvim
	  since: 2007-08
	  using: Vim 스크립트
	  license: GPLv2+
	  desc: |
		IME 없이도 [Vim](https://vim.org/)에서 한글(과 한자)을 입력할 수 있는 플러그인

	- title: 히마와리
	  link: /hmwr
	  since: 2012-10
	  until: 2015
	  using: Python
	  license: CC0
	  desc: |
		초절정 뻘소리 제조 IRC 봇

	- title: 나루 프로그래밍 언어
	  link: /naru
	  since: 2005
	  latest: r4.1
	  desc: |
		베이퍼웨어.

	- title: PyFunge
	  link: /pyfu
	  since: 2005
	  latest: 0.5-rc2
	  using: Python
	  license: MIT
	  desc: |
		파이썬 [Funge](w:en:Funge) 구현.

	- title: qr.js
	  link: /qrjs
	  since: 2011-01
	  using: JavaScript
	  license: CC0
	  desc: |
		자바스크립트만으로 만든 [QR 코드](w:QR 코드) 생성기

	- title: transdate
	  link: /trdt
	  since: 2005-03
	  latest: 1.1.1
	  using: Python
	  license: LGPLv2+
	  desc: |
		한국의 음력(태음태양력)을 `datetime.date`와 비슷한 인터페이스로 쓸 수 있는 라이브러리

	- title: 버섯 프로그래밍 언어
	  link: /vers
	  when: 2005-07
	  desc: |
		[비펀지](w:비펀지) 언어에서 스택을 덜어낸 난해한 프로그래밍 언어

- id: outdated
  title: 오래된 것들
  desc: |
	만들 때는 쓸모가 있었지만 지금은 그렇지 않아서 의미가 없는 것들.
	별로 쓰는 걸 권장하지 않습니다.
  entries:

	- title: <abbr title="DCinside Bugging Automaton">dcba</abbr>
	  link: bb:/dcba
	  when: 2009-09
	  using: Python
	  license: CC0
	  desc: |
		디시인사이드 파이썬 API. 템플릿 바뀌면서 망가졌음...

	- title: dcputhings
	  link: gh:/dcputhings
	  when: 2012-04
	  using: C, Ocaml
	  desc: |
		[0x10^c^](w:en:0x10c)의 (가상의) 16비트 프로세서 DCPU-16을 위한 도구들.
		DcpuAsm이라는 camlp4로 만든 어셈블리 DSL(!)이 있습니다.
		어차피 0x10^c^는 망했지만...

	- title: Delight
	  link: bb:/delight-core
	  since: 2008-04
	  until: 2009-06
	  using: D 1.0
	  desc: |
		[D](https://dlang.org/) 프로그래밍 언어가 아직 Phobos와 Tango 놓고 싸우고 있을 시절에
		Phobos를 유지하면서 얼마나 편하게 만들 수 있을까 궁금해서
		~~마침 병원에 있기도 해서 심심하기도 했고~~ 만든 대안 표준 라이브러리.
		흥미로운 코드가 있긴 하지만 아주 오래된 코드입니다. 특히 D2에서는 쓸모 없음.

	- title: DokuWiki-custom
	  link: /dwc
	  since: 2009-08
	  until: 2012-07
	  using: PHP
	  license: GPLv2
	  desc: |
		[도쿠위키](https://dokuwiki.org/)의 포크.
		개인 위키 용으로 쓰려고 이것 저것 플러그인과 파서를 고치고 나니 아까워져서 공개.
		여전히 여기 저기서 쓰고 있는 것 같긴 한데, 도쿠위키 템플릿 관련해서
		큰 변화가 있은 뒤로 따라잡질 못 해서 업데이트를 포기했습니다. **쓰지 마세요.**

	- title: js-iconv
	  link: bb:/js-iconv
	  since: 2008-10
	  using: JavaScript
	  license: MIT
	  desc: |
		cp949를 인코딩/디코딩하는 자바스크립트 라이브러리.
		이제 그냥 [`TextEncoder`](https://encoding.spec.whatwg.org/#interface-textencoder)랑
		[`TextDecoder`](https://encoding.spec.whatwg.org/#interface-textdecoder) 쓰세요.

	- title: Noty
	  link: bb:/noty
	  since: 2009-04
	  until: 2009-05
	  using: Python, Django
	  license: MIT
	  desc: |
		학교 팀프로젝트로 만들었던 RSS 리더 비스무리한 무언가.
		데스크탑 용으로 잘 포장한 웹앱으로, 일반적인 RSS 말고도 여러 사이트 및 대부분의 게시판을 자동으로 인식해서 해석하는 기능을 가지고 있었습니다.
		기술적으로나 실용적으로나 나쁘지 않았는데 불운한 사고로 프로젝트 점수는 별로 안 나온 불운의 소프트웨어.

	- title: theseit
	  link: bb:/theseit-main
	  since: 2005-09
	  until: 2008-01
	  using: C++, [SDL](https://libsdl.org/)
	  license: GPLv2+
	  desc: |
		멀티플랫폼 리듬게임으로 시작해서 거대한 멀티플랫폼 게임 엔진이 되어 버린 무언가.
		[Sonorous](/snrs)가 이 프로젝트의 정신적 후속작입니다.

	- title: TiniCube
	  link: bb:/tinicube
	  since: 2004-04
	  until: 2006-10
	  latest: g2 0.1.5.2
	  using: Python
	  license: GPLv2+
	  desc: |
		모듈화된 IRC 봇.
		원래는 SugarCube라는 다른 봇을 쓰다가 플러그인만 유지하고 새로 만든 것입니다.
		플러그인 낡은 거 빼면 사실 지금도 쓸 수 있지만...

	- title: TiniWiki
	  link: gh:/tiniwiki
	  since: 2004
	  latest: 0.1.-143pl1
	  using: PHP
	  license: CC0
	  desc: |
		작은 PHP 위키 엔진. 특이한 점이 몇 개 있긴 한데 이제 와서는 퇴물.

	- title: vlaah-python
	  link: bb:/vlaah-python
	  since: 2008-11
	  until: 2009-11
	  latest: 0.9.0
	  using: Python
	  license: MIT
	  desc: |
		VLAAH 웹 API의 파이썬 바인딩.
		지금은 VLAAH가 망했으므로 API 설계 정도나 쓸모 있습니다.

...
