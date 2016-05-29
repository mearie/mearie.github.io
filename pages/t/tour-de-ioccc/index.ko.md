---
title: Tour de IOCCC
date: 2015-09-08
lang: ko
short: occc
...

C로 프로그래밍을 좀 해 본 사람이라면 [IOCCC](http://ioccc.org/)라는 대회가 있다는 것을 알 지도 모르겠습니다. IOCCC, 즉 International Obfuscated C Code Contest는 난해한(obfuscated) C 코드를 겨루는 대회로 1984년부터 지금까지 꾸준히 계속 되고 있는 프로그래밍 컨테스트입니다. 이를테면 이런 코드지요.

    int i;main(){for(;i["]<i;++i){--i;}"];read('-'-'-',i+++"hell\
    o, world!\n",'/'/'/'));}read(j,i,p){write(j/p+p,i---j,i/i);}

"헉, 이게 무슨 코드야!"라고 생각하신다면 이 코드가 어떻게 돌아 가는지 [직접](1984-anonymous.html) 확인해 보시길 바랍니다. 적어도 잘못된 코드는 아닙니다.

난해한 코드는, 설령 가능하다 하더라도, 일면 쓸모 없어 보일 수 있습니다. 하지만 난해한 코드를 짜거나 해석하기 위해서는 프로그래밍 언어나 운영체제에 대한 깊은 지식이 필요하고, 난해한 코드를 짜는 다양한 기법들도 알려져 있기 때문에 결코 무시할 만한 것이 아닙니다. 이런 코드를 짤 수 있다는 것은 언어나 운영체제의 어두운 구석까지 잘 파악하고 있고, 따라서 그것들을 피해 가는 코드를 짤 수 있으며 비슷한 상황을 만났을 때 대처할 수 있다는 장점이 있지요. 그리고 무엇보다도 재미, 즉 만드는 사람에게 지적 및 기술적 희열을 안겨 주기도 합니다.

저는 이 글에서 IOCCC 수상작에 대한 자세한 설명을 하려고 합니다. 그래서 글 제목도 유명한 자전거 경기인 뚜르 드 프랑스(Tour de France)를 따라서 Tour de IOCCC라고 붙였습니다.[^1] 네. 물론 만든 사람도 많이 고생했겠지만 코드를 해석하는 것만으로도 상당한 노력이 필요하긴 합니다. 하지만, 일단 재밌지 않습니까? :)

[^1]: 뚜르 드 프랑스는 프랑스 및 인접국에서 매년 열리는 자전거 경기로 경기 거리가 3천에서 4천 킬로미터에 이르는 대규모 경기입니다. 거리가 거리이니만큼 완주에는 80~100시간이라는 긴 시간이 필요합니다. 암을 이기고 무려 일곱 번이나 연속으로 우승한 랜스 암스트롱의 일화로도 유명하지요.


# 일러두기

이 글을 읽기 위해서는 어느 정도의 C 프로그래밍 지식이 필요하며, 최소한 포인터와 비트 연산에 대한 이해가 필요합니다. (복잡한 예시에 대해서는 글에서 따로 설명하지만 그래도 개념 자체는 알고 있어야 합니다.) 또한 IOCCC는 유닉스 환경을 기본으로 하기 때문에 여기에 대한 이해가 있으면 좀 더 이해가 편합니다.

이 글은 [강 성훈](http://mearie.org/)이 썼으며, [크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 2.0 대한민국](http://creativecommons.org/licenses/by-nc-sa/2.0/kr/) 라이선스에 따라 비영리 목적으로 사용할 수 있습니다.[^2] 원본 코드의 저작권은 퍼블릭 도메인(public domain)에 속하여 저작권이 없습니다.

[^2]: IOCCC에서 수상한 소스 코드 및 포함된 데이터 파일을 제외한 나머지 저작물, 즉 힌트 파일(수상자와 심사위원의 코멘트)과 Makefile들은 다음과 같은 저작권 조항을 포함하고 있습니다.

    > Copyright © 2005, Landon Curt Noll, Simon Cooper, Peter Seebach and Leonid A. Broukhis. All Rights Reserved.
    >
    > Permission for personal, education or non-profit use is granted provided this copyright and notice are included in its entirety and remains unaltered. All other uses must receive prior permission in writing from the contest judges. 

        This is a code.
        This is a code.

    이 글은 IOCCC의 힌트 파일을 통째로 번역하거나 하지는 않지만, 단순 인용의 한계가 명확하지 않으므로 가능한한 문제를 피하기 위해 비영리 조항을 포함하고 있습니다. 만약 영리적 목적으로 사용하고 싶을 경우 저(강 성훈)와 IOCCC 심사위원들에게 각각 연락하시길 바랍니다.

이 글의 원본은 [머큐리얼 저장소](http://hg.mearie.org/document/tour-de-ioccc/)에서 작업되고 있습니다. HTML 변환을 위해서는 [pandoc](http://johnmacfarlane.net/pandoc/)이 필요합니다. 혹시 도움을 주실 수 있는 분께서는 미리 저에게 연락하시거나 머큐리얼 저장소를 복제(`hg clone`)한 뒤 작업 후 알려 주시면 제가 반영하도록 하겠습니다.


# 시작하기 전에

* <s>[개발 환경 만들기](start-environment.html)</s>
* <s>[자주 쓰이는 기법들](start-techniques.html)</s>
* [옛날의 C 언어](start-legacy.html)


# 1회: 1984년

* [anonymous](1984-anonymous.html) (2009-01-14)
* [decot](1984-decot.html) (2009-01-18)
* <s>[laman](1984-laman.html)</s>
* [mullender](1984-mullender.html) (2009-01-18 *TODO*)


# 2회: 1985년

* <s>[applin](1985-applin.html)</s>
* <s>[august](1985-august.html)</s>
* <s>[lycklama](1985-lycklama.html)</s>
* <s>[shapiro](1985-shapiro.html)</s>
* [sicherman](1985-sicherman.html) (2009-01-17)


# 3회: 1986년

* <s>[applin](1986-applin.html)</s>
* <s>[august](1986-august.html)</s>
* <s>[bright](1986-bright.html)</s>
* <s>[hague](1986-hague.html)</s>
* <s>[holloway](1986-holloway.html)</s>
* <s>[marshall](1986-marshall.html)</s>
* <s>[pawka](1986-pawka.html)</s>
* [stein](1986-stein.html) (2009-01-20)
* <s>[wall](1986-wall.html)</s>


# 4회: 1987년

* <s>[biggar](1987-biggar.html)</s>
* <s>[heckbert](1987-heckbert.html)</s>
* <s>[hines](1987-hines.html)</s>
* <s>[korn](1987-korn.html)</s>
* <s>[lievaart](1987-lievaart.html)</s>
* <s>[wall](1987-wall.html)</s>
* <s>[westley](1987-westley.html)</s>


# 5회: 1988년

* <s>[applin](1988-applin.html)</s>
* <s>[dale](1988-dale.html)</s>
* <s>[isaak](1988-isaak.html)</s>
* [litmaath](1988-litmaath.html) (2009-01-18)
* <s>[phillipps](1988-phillipps.html)</s>
* <s>[reddy](1988-reddy.html)</s>
* <s>[robison](1988-robison.html)</s>
* [spinellis](1988-spinellis.html) (2009-01-18)
* <s>[westley](1988-westley.html)</s>


# 6회: 1989년

* <s>[fubar](1989-fubar.html)</s>
* <s>[jar.1](1989-jar.1.html)</s>
* <s>[jar.2](1989-jar.2.html)</s>
* <s>[ovdluhe](1989-ovdluhe.html)</s>
* <s>[paul](1989-paul.html)</s>
* <s>[robison](1989-robison.html)</s>
* <s>[roemer](1989-roemer.html)</s>
* <s>[tromp](1989-tromp.html)</s>
* <s>[vanb](1989-vanb.html)</s>
* <s>[westley](1989-westley.html)</s>


# 7회: 1990년

* <s>[baruch](1990-baruch.html)</s>
* <s>[cmills](1990-cmills.html)</s>
* <s>[dds](1990-dds.html)</s>
* <s>[dg](1990-dg.html)</s>
* <s>[jaw](1990-jaw.html)</s>
* <s>[pjr](1990-pjr.html)</s>
* <s>[scjones](1990-scjones.html)</s>
* <s>[stig](1990-stig.html)</s>
* <s>[tbr](1990-tbr.html)</s>
* <s>[theorem](1990-theorem.html)</s>
* <s>[westley](1990-westley.html)</s>


# 8회: 1991년

* <s>[ant](1991-ant.html)</s>
* <s>[brnstnd](1991-brnstnd.html)</s>
* <s>[buzzard](1991-buzzard.html)</s>
* <s>[cdupont](1991-cdupont.html)</s>
* <s>[davidguy](1991-davidguy.html)</s>
* <s>[dds](1991-dds.html)</s>
* <s>[fine](1991-fine.html)</s>
* <s>[rince](1991-rince.html)</s>
* <s>[westley](1991-westley.html)</s>


# 9회: 1992년

* <s>[adrian](1992-adrian.html)</s>
* <s>[albert](1992-albert.html)</s>
* <s>[ant](1992-ant.html)</s>
* <s>[buzzard.1](1992-buzzard.1.html)</s>
* <s>[buzzard.2](1992-buzzard.2.html)</s>
* <s>[gson](1992-gson.html)</s>
* <s>[imc](1992-imc.html)</s>
* <s>[kivinen](1992-kivinen.html)</s>
* <s>[lush](1992-lush.html)</s>
* <s>[marangon](1992-marangon.html)</s>
* <s>[nathan](1992-nathan.html)</s>
* <s>[vern](1992-vern.html)</s>
* <s>[westley](1992-westley.html)</s>


# 10회: 1993년

* <s>[ant](1993-ant.html)</s>
* <s>[cmills](1993-cmills.html)</s>
* [dgibson](1993-dgibson.html) (2009-01-20 *TODO*)
* <s>[ejb](1993-ejb.html)</s>
* <s>[jonth](1993-jonth.html)</s>
* <s>[leo](1993-leo.html)</s>
* <s>[lmfjyh](1993-lmfjyh.html)</s>
* <s>[plummer](1993-plummer.html)</s>
* <s>[rince](1993-rince.html)</s>
* <s>[schnitzi](1993-schnitzi.html)</s>
* <s>[vanb](1993-vanb.html)</s>


# 11회: 1994년

* <s>[dodsond1](1994-dodsond1.html)</s>
* <s>[dodsond2](1994-dodsond2.html)</s>
* <s>[horton](1994-horton.html)</s>
* <s>[imc](1994-imc.html)</s>
* <s>[ldb](1994-ldb.html)</s>
* <s>[schnitzi](1994-schnitzi.html)</s>
* <s>[shapiro](1994-shapiro.html)</s>
* [smr](1994-smr.html) (2009-01-17)
* <s>[tvr](1994-tvr.html)</s>
* <s>[weisberg](1994-weisberg.html)</s>
* [westley](1994-westley.html) (2009-01-20)


# 12회: 1995년

* <s>[cdua](1995-cdua.html)</s>
* <s>[dodsond1](1995-dodsond1.html)</s>
* <s>[dodsond2](1995-dodsond2.html)</s>
* <s>[esde](1995-esde.html)</s>
* <s>[garry](1995-garry.html)</s>
* [heathbar](1995-heathbar.html) (2009-01-18)
* <s>[leob](1995-leob.html)</s>
* <s>[makarios](1995-makarios.html)</s>
* <s>[savastio](1995-savastio.html)</s>
* <s>[schnitzi](1995-schnitzi.html)</s>
* <s>[spinellis](1995-spinellis.html)</s>
* <s>[vanschnitz](1995-vanschnitz.html)</s>


# 13회: 1996년

* <s>[august](1996-august.html)</s>
* <s>[dalbec](1996-dalbec.html)</s>
* <s>[eldby](1996-eldby.html)</s>
* <s>[gandalf](1996-gandalf.html)</s>
* <s>[huffman](1996-huffman.html)</s>
* <s>[jonth](1996-jonth.html)</s>
* <s>[rcm](1996-rcm.html)</s>
* <s>[schweikh1](1996-schweikh1.html)</s>
* <s>[schweikh2](1996-schweikh2.html)</s>
* <s>[schweikh3](1996-schweikh3.html)</s>
* <s>[westley](1996-westley.html)</s>


# 14회: 1998년

* <s>[banks](1998-banks.html)</s>
* <s>[bas1](1998-bas1.html)</s>
* <s>[bas2](1998-bas2.html)</s>
* <s>[chaos](1998-chaos.html)</s>
* <s>[df](1998-df.html)</s>
* <s>[dlowe](1998-dlowe.html)</s>
* <s>[dloweneil](1998-dloweneil.html)</s>
* <s>[dorssel](1998-dorssel.html)</s>
* <s>[fanf](1998-fanf.html)</s>
* <s>[schnitzi](1998-schnitzi.html)</s>
* <s>[schweikh1](1998-schweikh1.html)</s>
* <s>[schweikh2](1998-schweikh2.html)</s>
* <s>[schweikh3](1998-schweikh3.html)</s>
* <s>[tomtorfs](1998-tomtorfs.html)</s>


# 15회: 2000년

* <s>[anderson](2000-anderson.html)</s>
* <s>[bellard](2000-bellard.html)</s>
* <s>[bmeyer](2000-bmeyer.html)</s>
* <s>[briddlebane](2000-briddlebane.html)</s>
* [dhyang](2000-dhyang.html) (2009-01-15)
* <s>[dlowe](2000-dlowe.html)</s>
* <s>[jarijyrki](2000-jarijyrki.html)</s>
* [natori](2000-natori.html) (2009-01-17)
* <s>[primenum](2000-primenum.html)</s>
* <s>[rince](2000-rince.html)</s>
* <s>[robison](2000-robison.html)</s>
* <s>[schneiderwent](2000-schneiderwent.html)</s>
* <s>[thadgavin](2000-thadgavin.html)</s>
* <s>[tomx](2000-tomx.html)</s>


# 16회: 2001년

* <s>[anonymous](2001-anonymous.html)</s>
* <s>[bellard](2001-bellard.html)</s>
* <s>[cheong](2001-cheong.html)</s>
* [coupard](2001-coupard.html) (2009-01-19 *TODO 코드 분석만 완료*)
* <s>[ctk](2001-ctk.html)</s>
* <s>[dgbeards](2001-dgbeards.html)</s>
* <s>[herrmann1](2001-herrmann1.html)</s>
* <s>[herrmann2](2001-herrmann2.html)</s>
* <s>[jason](2001-jason.html)</s>
* <s>[kev](2001-kev.html)</s>
* <s>[ollinger](2001-ollinger.html)</s>
* <s>[rosten](2001-rosten.html)</s>
* <s>[schweikh](2001-schweikh.html)</s>
* <s>[westley](2001-westley.html)</s>
* <s>[williams](2001-williams.html)</s>


# 17회: 2004년

* <s>[anonymous](2004-anonymous.html)</s>
* <s>[arachnid](2004-arachnid.html)</s>
* <s>[burley](2004-burley.html)</s>
* <s>[gavare](2004-gavare.html)</s> (*예약*)
* <s>[gavin](2004-gavin.html)</s>
* [hibachi](2004-hibachi.html) (2009-01-18)
* <s>[hoyle](2004-hoyle.html)</s>
* <s>[jdalbec](2004-jdalbec.html)</s>
* [kopczynski](2004-kopczynski.html) (2009-01-28 *TODO*)
* <s>[newbern](2004-newbern.html)</s>
* <s>[omoikane](2004-omoikane.html)</s>
* <s>[schnitzi](2004-schnitzi.html)</s>
* <s>[sds](2004-sds.html)</s>
* <s>[vik1](2004-vik1.html)</s>
* <s>[vik2](2004-vik2.html)</s>


# 18회: 2005년

* <s>[aidan](2005-aidan.html)</s>
* <s>[anon](2005-anon.html)</s>
* <s>[boutines](2005-boutines.html)</s>
* <s>[chia](2005-chia.html)</s>
* <s>[giljade](2005-giljade.html)</s>
* <s>[jetro](2005-jetro.html)</s>
* <s>[klausler](2005-klausler.html)</s>
* <s>[mikeash](2005-mikeash.html)</s>
* <s>[mynx](2005-mynx.html)</s>
* <s>[persano](2005-persano.html)</s>
* <s>[sykes](2005-sykes.html)</s>
* [timwi](2005-timwi.html) (2009-01-28)
* <s>[toledo](2005-toledo.html)</s>
* <s>[vik](2005-vik.html)</s>
* <s>[vince](2005-vince.html)</s>


# 19회: 2006년

다음 목록은 [2007년 발표 자료](http://decoded.org.ua/files/presentations/ioccc-2006-v024.key.pdf)를 토대로 만들어진 것입니다. 소스 코드는 2009년 1월 현재까지 완전히 공개되어 있지 않습니다.

* <s>[birken](2006-birken.html)</s>
* <s>[borsanyi](2006-borsanyi.html)</s>
* <s>[grothe](2006-grothe.html)</s>
* <s>[hamre](2006-hamre.html)</s>
* <s>[meyer](2006-meyer.html)</s>
* <s>[monge](2006-monge.html)</s>
* <s>[night](2006-night.html)</s>
* <s>[sloane](2006-sloane.html)</s>
* <s>[stewart](2006-stewart.html)</s>
* <s>[sykes1](2006-sykes1.html)</s>
* <s>[sykes2](2006-sykes2.html)</s>
* [toledo1](2006-toledo1.html) (2009-03-08 *TODO*)
* <s>[toledo2](2006-toledo2.html)</s>
* <s>[toledo3](2006-toledo3.html)</s>


