---
title: EUC-KR
short: euck
...

[[KS X 1001]]을 사용하는 [[문자 인코딩]]. 현재 [[대한민국]]에서 [[UTF-8]]을 빼고 가장 널리 쓰이는 문자 인코딩이다. ~~만약 [[ISO 2022-KR|다른 인코딩]]이 쓰이기나 한다면 말이지...~~

[[EUC]] 계열 문자 인코딩 중 가장 단순하여, 정확히 두 개의 [[문자 집합]]을 포함하고 있다:

* CR(`20`--`7F`)에 [[KS X 1003]] (= [[ISO/IEC 646]]:KR)
* GR(`A0`--`FF`)에 [[KS X 1001]]

당연히 KS X 1001만이 포함되었으므로 모든 [[현대 한글]]을 표현할 수는 없다("완성형"이라고 부르는 이유 중 하나). 아니, 좀 더 엄밀하게는 조합 문자를 사용하면 표현은 가능하지만 실질적으로 지원하는 곳은 없다.

# [[Windows-949]]의 또 다른 이름

앞에서 설명한 이유 때문에 **실질적으로** EUC-KR이라고 부르는 거의 모든 문자 인코딩은 사실 "확장완성형", 즉 [[Windows-949]]으로 GL(`80`--`9F`)과 GR 영역을 마구 섞는 방법을 통해 기존에 지원되지 않던 한글을 모두 지원하는 초강수를 두게 된다. (EUC는 [[ISO 2022]]의 변형이기 때문에 당연히 이런 형태의 사용은 표준이 아니다.)

[[모질라]]는 한동안 EUC-KR을 곧이 곧대로 해석해서 KS X 1001에 없는 한글을 조합 문자를 사용해서 표기하여 다른 브라우저에서는 깨지는(...) 안습한 사태를 만들어 낸 바 있으며, [[인터넷 익스플로러]] 옛 버전은 한 술 더 떠서 사용 불가능한 문자를 **HTML 엔티티로 표현**하는 말도 안 되는 동작을 보인다. (여기까지면 차라리 좋겠지만, 일부 웹 애플리케이션들은 이 엔티티를 해석하기 위해서 **텍스트를 HTML로 해석하는** 섬뜩한 일까지 벌였다.) 덕택에 EUC-KR은 [[HTML5]] 표준에서 예외적으로 인코딩 선언을 무시하는 [첫번째 케이스](http://www.whatwg.org/specs/web-apps/current-work/multipage/parsing.html#character-encodings-0)로 등록되어 있다(뭐 사실은 알파벳 순이라서겠지만).

