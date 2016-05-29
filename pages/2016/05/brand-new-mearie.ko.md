---
template: journal
lang: ko
date: 2016-05-29
short: Pj04
...

메아리 새 버전을 만들었다. 뭐 그렇다고.

현재 남아 있는 문제:

* table of contents
* per-year journal archive
* 저널 다음/이전 글
* `#more` 타겟에 세로 위치가 제대로 반영되어 있지 않은 것 같음 (section에 붙은 건 되는데)
* 사이트맵에 제목 없으면 summary 나오게 하는 것 (가능한가?)
* `pre` 등의 스타일링 변경: 최대한 배경을 안 쓰게 하는 방향으로, print media에서 개판 됨. 그리고 문법 강조 등 라이브러리랑도 상성이 잘 안 맞음
* 저널 notes 가져오기
* 메타데이터 블록 스타일링. 원래는 맨 뒤에 밀어 넣으려고 했는데 앞으로 빼내야 겠다 (e.g. 이 글 읽는데 몇 분)
* afternote, block `ins`/`del` 등의 스타일링이 빠져 있음. 저널 글 가져 올 거면 분명 여기서 문제 생김
* print media에서 short url로 스타일링되게 (이럴려면 postprocess할 때 원 short url을 남겨야 함. 좀 고쳐야)
* 메타데이터 날짜 자동 파싱 (현재는 verbatim)
* 사이트맵 커질 경우를 대비해서 grouping...

