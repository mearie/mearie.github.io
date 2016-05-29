---
template: journal
lang: ko
date: 2016-03-11 #T22:31:05+09:00
short: Pj02
redirect-from: post/140853939603
...

[알파고](https://en.wikipedia.org/wiki/AlphaGo)가 [이세돌](https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%84%B8%EB%8F%8C)을 상대로 2승을 따냈다. 바(둑)알(지)못(하는 사람)인 나조차 중계 방송을 지켜 봤을 정도인데, 아마도 앞으로는 더 이상 실시간으로 중계 방송을 보지 않을 것이다. 일단 업무시간에 집중을 할 수 없고(…) 안타깝긴 해도 이세돌이 처참하게 박살나는 이 상황이 근시일 내에 올 것은 명백했기 때문이다. 앞으로의 대국은, 딥마인드 측이 밝힌 의도마냥, 알파고가 이세돌과 비교했을 때 얼마나 더 잘 두는가의 범위를 추정하는 작업이 될 것이다.[^1] 이 자리를 빌어 이세돌에게 심심한 위로를.[^3]

[^1]: 많이 안 쓰는 것 같지만, 바둑에서도 [Elo 레이팅](https://en.wikipedia.org/wiki/Elo_rating)을 적용한 [자료](http://www.goratings.org/)가 있다(정확히는 Elo와는 달리 업데이트 모델이 다르지만 수치의 상관은 동일하다). 이에 따르면 이세돌의 3월 11일 현재 레이팅은 [3525](http://www.goratings.org/players/5.html). 만약 최적 컨디션의 이세돌과 알파고를 계속 맞붙였을 때 평균 승률이 20%:80%면 알파고의 레이팅은 240 높은 **3760**이어야 하고, 이 숫자는 지금껏 지구상의 어떤 바둑 기사도 근접한 적이 없는 수치이다. 비교를 위해, 이미 컴퓨터가 인간을 갖고 노는 체스에서 [최강의 소프트웨어](https://en.wikipedia.org/wiki/Chess_engine#Ratings)와 [역사상 최강의 인간 플레이어](https://en.wikipedia.org/wiki/Comparison_of_top_chess_players_throughout_history#Statistical_methods) 사이의 레이팅 차이는 400 안팎으로 추정된다(물론 더 이상 인간-컴퓨터가 공식적으로 맞붙는 일은 없으므로 어디까지나 추정).

[^3]: (이 글을 쓰고 이틀 뒤 이세돌이 4국에서 알파고를 이겼다. 이는 알파고의 방법론이 얼마나 인간의 방법론과 유사한지를 보여 주는, 그리고 당연하게도 알파고가 바둑을 완벽하게 풀어 버리는 알고리즘은 아님을 다시금 확인해 주었다고 본다. 이세돌에게나 **구글 딥마인드 측에나** 다행인 결과가 아닐 수 없다.)

알파고가 다른 모든 이슈를 날려버리고 뉴스 헤드라인에 떡하니 박혀 있는 건 좋은 일이라고 생각하지만(이런 일이 흔치 않으니까), 예상했듯 이게 도대체 무슨 의미를 가지는가에 대해서 제대로 짚고 있는 사람은 많지 않다. 그러하니 이게 **나한테** 무슨 의미를 지니는지 코멘트해 보겠다. 아마 다른 사람들은 다르게 생각하겠지만 이 생각이 다른 사람들에게 영향을 준다면 기쁠 것이다.

# 바둑

다들 예상하듯이 현재 바둑계는 얼이 빠진 상태이다. 하나 부연을 해 두자면, 체스도 그런 면이 있긴 했지만 바둑계는 바둑을 “일반화했을 때 [EXPTIME](https://en.wikipedia.org/wiki/EXPTIME)-complete한 존나 어려운 조합적 완전정보 제로섬 보드 게임”으로 보는 게 아니고 인생을 반영하는 무언가 철학적인 물건으로 보는 경향이 있다. 나는 이런 주장을 들을 때마다 [클라나드](https://namu.wiki/w/CLANNAD)가 [인생](https://namu.wiki/w/%ED%8E%98%EC%9D%B4%ED%8A%B8%EB%8A%94%20%EB%AC%B8%ED%95%99%20%EC%83%88%EC%9D%98%20%EC%8B%9C%EB%8A%94%20%EA%B5%AD%EA%B0%80%20%ED%81%B4%EB%9D%BC%EB%82%98%EB%93%9C%EB%8A%94%20%EC%9D%B8%EC%83%9D#s-3)이라는 말이 떠오른다.

아, 물론 클라나드는 인생이다. 그러니 바둑도 인생이다.

아니 농담하는 게 아니고, 잘 생각해 보자. 왜 존나 어려운 보드 게임에 이런 수식어가 붙었을까? 나는 인간이 완벽하게 두는 게 불가능한 게임을 인간이 어떻게든 체계화시켜서 인간들끼리 두니까 이런 생각을 하게 된 것이라고 생각한다. 마치 생명체의 조건에 대해서 잘 모르는 상태에서 인간 비스무리한 게 살 수 있는 [생명체 거주 가능 구역](https://en.wikipedia.org/wiki/Circumstellar_habitable_zone)을 중심으로 외계 생명을 탐색하려는 시도를 보는 것 같달까.

바둑을 둬서 상대에 대해 알 수 있다는 것은 순전히 인간이 바둑을 두는 알고리즘이 그런 정보를 유추할 수 있을 정도로 정보를 많이 노출한다는 거지, 바둑이 그런 성질을 가지고 있다는 얘기는 아니다. 그러나 이런 점에서 알파고의 “기풍”을 두고 사람들이 설왕설래하는 것은 참 흥미로운데, 왜냐하면 바둑을 통해 드러나는 “기풍”을 통해 상대를 추측하듯이 우리는 매 순간 제한된 시청각 정보로 상대를 추측하고 있기 때문이다. (애당초 인간의 마음이라는 것 자체도 외부 신호에서 추론되는 것이지 마음이라는 분명한 존재가 있다는 보장이 없다.) 요컨대 우리는 바둑을 통한 [튜링 테스트](https://en.wikipedia.org/wiki/Turing_test)를 하고 있는 셈이다. 튜링 테스트를 했더니 상대방이 인간은 아닌 것 같은데 사실 신이었다는 게 웃긴 점이지만.

당연하겠으나 앞으로 바둑은 많이 바뀔 것이다. 후술하겠으나 인간의 특성 중에서 직관을 더 잘 구현하기만 하면 최소 인간만큼 바둑을 둘 수 있다는 게 명백해졌으니, 인간끼리만 대국하며 형성된 확증편향(confirmation bias)은 많이 나아질 것이다(나아지지 못 한다면 그것이 바둑이라는 게임의 종말일 것이다). 체스에서 그랬듯이, 바둑 소프트웨어가 꾸준히 발전한다는 전제 하에 이를 활용하여 편견이 덜한 저연령의 기사들이 대회를 주름잡을 것이고, 물론 이걸로 [부정행위를 저지르는 사람](https://en.wikipedia.org/wiki/Borislav_Ivanov)도 생기겠지. 바둑 자체는 수천년간 잘 해 온 게임이니만큼 사라지진 않을 것이되, 그간 인간의 선입견에 의해 붙은 각종 수식어에서 해방된, 진정한 의미에서의 보드 게임으로서 남게 될 것이다.

# 알파고

알파고에 대해서는 수많은 오해가 쌓이고 있는 것 같은데, 뭐, 보통 사람이라면 어쩔 수 없다 싶긴 하다. 구체적인 예: 알파고느님을 찬양하자(약인공지능과 강인공지능을 구분하지 못함), 알파고는 GPU를 쓰기 때문에 컴퓨터가 못 보는 시각적인 정보를 처리할 수 있음(어처구니 없긴 한데, 물론 알파고가 필요로 하는 연산이 GPU로 하는 게 더 싸서이기 때문), 판 후이 때보다 훨씬 더 성능이 높다(보도에 혼선이 있어서 약간 성능이 높은 건 사실인 듯 하나, 그렇다고 승률이 비약적으로 올라가진 않음), 알파고는 이전 대국으로부터 학습하여 강해짐(마찬가지로 구글 측에서 안 쓰겠다고 언급했고, 어차피 대국 갯수가 5개라 학습의 효과가 별로 없으며 주화입마[overfitting]의 위험이 큼), 알파고는 수만건의 기보를 학습해서/수천대의 컴퓨터를 사용해서 강하다(실제 근본적인 이유는 자기 자신과의 대국을 통한 강화학습), **구글이 알파고 로봇도 만들었다**(…물론 대신 놔 주는 사람은 [네이처 논문](www.nature.com/nature/journal/v529/n7587/full/nature16961.html) 제 1저자인 아자 황) 등등등.

이런 모든 오해들을 차치하고, 나는 알파고를 **인간의 방법론을 인간보다 잘 따르는** 프로그램이라고 정의해야 한다 생각한다. 역사적으로 조합적이고(유한한 수의 바둑판 상태로부터 최적의 수를 뽑아야 하고) 완전정보(서로 바둑판 전체를 다 볼 수 있으며) 제로섬인(한쪽이 승리하면 다른쪽이 패배하는) 보드 게임을 컴퓨터가 접근하는 방법은 대략 다음과 같이 발전해 왔다.

* [미니맥스](https://en.wikipedia.org/wiki/Minimax) 계열 알고리즘들은, 상대방이 최선의 수(즉 나한테 최악의 결과를 주는 수)를 찍는다는 전제 하에 그 최적의 수가 상대방 입장에서 최악이 되도록(즉 내가 입을 손해가 최소가 되도록) 하는 수를 선택하려고 한다. 간단명료하긴 하지만 게임이 조금만 복잡해도 탐색해야 하는 수의 숫자가 기하급수적으로 늘어난다. 따라서 다양한 최적화와 경험적 지식으로 이 숫자를 줄이려고 노력했는데, 사실 **체스는 이걸로 뚫렸지만** 바둑은 요원했다.
* [몬테카를로 트리 탐색](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)(MCTS) 계열 알고리즘들은 상당히 다른 접근을 취한다. 모든 가능성을 탐색하려고 하지 않고, 랜덤하게 모의 플레이를 계속해서 이기는 수에는 가중치를 주어 그 수로 시작하는 게임을 더 탐색할 기회를 준다. 충분히 탐색했다 싶으면 가장 많이 선택된 수를 선택한다. 모의 플레이 자체는 완전 랜덤하기 때문에 전혀 지능적이지 않음에도 불구하고, 같은 자원을 투자하고도 미니맥스 계열보다 훨씬 깊은 수를 탐색해 볼 수 있고 경험적 지식을 덜 필요로 하기 때문에 경제적이라는 게 알려지면서 바둑 소프트웨어들에서 각광을 받았다.
* 위에서 이기는 수는 “그 수로 시작하는 게임을 더 탐색할 기회를 받는다”고 했는데 이 기회를 어떻게 활용하느냐가 알파고의 결정적인 장점이다. 기존의 바둑 소프트웨어들은 [UCT](http://senseis.xmp.net/?UCT)라고 부르는 적절히 괜찮아 보이는 경험적 방법을 따랐다. 그러나 알파고는 요즘 뜨다 못해 성층권으로 날아가고 있는 [딥 러닝](https://en.wikipedia.org/wiki/Deep_learning) 방법론을 적용해, 어느 수를 먼저 시험해 봐야 할지, 그리고 모의 플레이를 안 해 보고도 그 결과가 어떻게 될지를 추측하고 학습한다. 딥 러닝 자체는 무척 강력하면서도 무척 제약이 많은 방법론이지만(그러므로 딥 러닝 hype는 항상 경계할 필요가 있다), 적어도 특정 상황에서 무엇이 “중요”한지에 대한 지식을 학습하는 데는 큰 도움이 된 것이다.

몹시 흥미롭게도, 인간의 방법론은 (컴퓨터만치 연산량이 많지 않다는 것만 빼면) 이러한 일련의 알고리즘 발전과 유사한 점이 많다. 인간은 애초에 모든 가능성을 탐색하는 게 어려웠기 때문에 일찍이 바둑판을 어떻게 분석해야 유리한지를 수만 수억판의 (사람과의) 대국을 통해 연구해 왔고, 그 결과가 “정석”으로 불리는 알고리즘이다. 그러나 정석은 앞에서도 언급했듯, 무슨 루빅 큐브를 풀듯 바둑을 “푸는” 알고리즘이 아니기 때문에 정석에서 벗어나야 할 때가 있는데, 이를 대표하는 낱말이 선천적 지능과 후천적 경험을 통해 형성되는 “직관”과 “창의성”이다. 이 낱말들을 정의를 거의 안 하고 써서 자꾸 간과하지만, 사실 직관이라 함은 그냥 말로 설명하기 어려운 경험적 알고리즘이고, 창의성은 그 알고리즘에서 언제 벗어나서 통상적인 탐색 방법으로 회귀해야 할지를 알려 주는 또 다른 경험적인 알고리즘인 것이다.

알파고의 입장에서 정석은 처음에 신경망들을 초기화할 때 사용되었던 기보들이다. 물론 알고리즘의 형태로 전달되는 정석과는 달리 이 기보들은 그냥 “괜찮은 플레이”들의 목록일 뿐이지만, 대신 알파고는 (마치 인간들이 수천년간 해 왔듯이!) 자기 자신과의 강화학습(reinforcement learning)을 통해 이 기보들에서 무슨 의미를 뽑아내야 할지를 알아낸다. 자신만의 직관을 형성한 알파고는 그 직관을 따르되 “필요하면” 직관이 가리키는 수를 더 파고 들어간다(물론 이게 언제 필요한지 또한 학습된다). 인간이라고 이렇게 못 할 이유는 없다---생물학적으로 (인간이 수만년을 동일한 지능으로 살 수는 없을테니) 그리고 윤리적으로 (아무 것도 모르고 바둑만 두는 어린이를 인간 사회가 용납할 수 있겠는가?) 무리일 뿐.

내가 판 후이가 졌다는 소식을 들은 뒤 바둑이 2~3년 안에 정복될 거라고 생각한 이유도 이것 때문으로, 인간의 직관만을 더 모델링하는 것으로 바둑을 인간만치 둘 수 있다면 인간과는 달리 기계는 스케일링할 수 있기 때문이다. 실제로는 다섯 달 걸렸으니 내 예측 실력은 별로인듯 하다.

# 인공지능

알파고 덕분에 뉴스에서 맨날 인공지능에 대해서 떠들어 대는 게 나는 개인적으로 흐뭇(?)하다. 오개념이야 어쨌든, 인공지능의 중요성에 대해서 온 국민이 깨달으면 그 다음에 진지한 논의를 시도할 수는 있을테니까 말이다. 하지만 그래도 이건 짚고 넘어 가야지.

**난 인공지능이 인간의 지능을 따라잡기 전에 인간이 자기 스스로를 멸망시킬 가능성이 더 높다고 생각한다.**

이른바 [존재의 위험](https://en.wikipedia.org/wiki/Existential_risk)이라는 개념이 존재한다. 나는 이 말을 “존재로 인한 위험”으로 해석하는 게 더 와닿는다고 생각하는데, 이는 인류가 존재하기 **때문에** 의미가 생긴 위험이기 때문이다(지구에 소행성 좀 충돌한다고 지구가 박살나진 않는다---인류 문명이 아작날 뿐). 존재의 위험은 여러 종류가 있는데, 이른바 특이점을 믿는 사람들은 인공지능이 가장 큰 위험이라고 생각하는 경향이 있다. 진실은, 우리는 아무 것도 아는 게 없다. 물론 몇 번 문명이 박살나 본 뒤에 그 결과가 기록되면 대략의 윤곽이 드러나긴 하겠지만, 우리는 박살난 적이 없거나 박살났어도 그 결과를 가지고 있지 않다;;; [인류 원리](https://en.wikipedia.org/wiki/Anthropic_principle)는 많은 사람들이 꺼림칙하다고 느끼는 논리긴 하지만 이 정도로 자료가 없으면 인류 원리가 최선의 논리가 될 수 밖에 없다.

그럼에도 불구하고 내가 이렇게 생각하는 것은 인공지능은 위험을 유발하기 까지는 좀 시간이 남아 있는 반면, 인류 문명을 박살낼 수 있는 병기는 이미 충분히 많이 존재하는 데다, 이 병기의 활성화를 위해 필요한 명령 체인이 대부분 **인간**이라는 전혀 믿을만하지 않은 컴포넌트 몇 개 정도로 구성되어 있기 때문이다. 아이러니하게도 인간이 믿을만하지 못하다는 인식은 역설적으로 인공지능을 포함해 인간이 아닌 것들에게 인간이 전통적으로 해 왔던 일들을 맡기면서 생긴 것이니, 이 또한 인공지능과 연결되어 있는 주제라 하겠다.

인공지능으로 돌아가면, 우리는 흔히 특정 목적을 위해 만들어진/학습시킨 약인공지능과 인간과 비견되는 강인공지능을 구분해서 말한다. 이 논리를 진전시키면 당연하게도 약인공지능은 인류의 위협이 될 수 없고, 강인공지능이 만들어질 정도의 문명이 되면 강인공지능이 **무조건** 만들어질 것이므로 이를 대비해야 한다…는 결론이 나온다. 이 논리를 충실히 따르는 [재밌는 글](https://coolspeed.wordpress.com/2016/01/03/the_ai_revolution_1_korean/)이 있으니 안 읽어 보신 분은 한 번 읽어 보고 돌아 오시라.

이 논리는 재밌긴 하지만 강력한 문제가 하나 있다. 알파고가 앞에서 바둑을 통해 튜링 테스트를 통과했다는 얘기를 잠깐 했었다. 그런데 튜링 테스트는 일반적으로 강인공지능의 필수 조건 중 하나라고 받아들여지는데, 그럼 알파고는 강인공지능이란 말인가? 아니다. 알파고 논문을 보면 알 수 있지만 알파고에 경험적 알고리즘이 아예 안 들어간 것은 아니다. 예를 들어서 [축](http://senseis.xmp.net/?Ladder)의 개념은 알파고가 학습한 게 아니라 기본 특징(feature)으로 미리 제공된 것이다. 물론 인간의 뇌도 이러한 특수 목적의 회로를 갖고 있다는 의심을 계속 받고 있지만[^2] 어쨌든 외부에서 충분한 입력을 미리 주지 않으면 돌아가질 않으니 강인공지능의 정의에는 위배되는 것 같아 보인다. 아니, 잠깐, 뭔가 이상하지 않은가?

[^2]: 예를 들어서 [스티븐 핑커](https://en.wikipedia.org/wiki/Steven_Pinker) 같은 사람의 주장에 따르면, 인간은 언어적 지식을 가지고 태어나진 않지만 언어를 쉽게 배울 수 있는 **메타 지식**을 위한 회로가 [뇌에 박혀 있다](https://en.wikipedia.org/wiki/Steven_Pinker#Human_cognition_and_natural_language)는 것이다. 물론 반론도 엄청 많다.

이런 이상한 결과는 약인공지능과 강인공지능이 칼로 깔끔하게 잘라 구분할 수 있는 거라고 생각했기 때문에 나온다. 실제로는, 약인공지능도, 그리고 **약인공지능조차 못 한 알고리즘도**, 조건을 충분히 제약하면 인간이 나타내는 지능의 징표를 얼마든지 보일 수 있다. [뢰브너 상](https://en.wikipedia.org/wiki/Loebner_Prize)이라고 해서, 정해진 시간동안 채팅을 통해 튜링 테스트를 해서 가장 인간처럼 보이는 프로그램을 뽑는 대회가 있다. 튜링 테스트가 매우 중요한 것이라고 생각했던 옛날에는 뢰브너 상을 통해 궁극적으로 인간과 동등한 인공지능이 가능할 것이라는 ~~헛된~~ 희망이 있었다. 1996년에 [HeX](http://www.nyu.edu/gsas/dept/philo/courses/mindsandmachines/Papers/hutchens96how.pdf)라는, 호주 사람인 척 하면서 상대방의 질문에 딴소리와 도발로 일관하는 프로그램이 수상하기 전까지는 말이다! 물론 일반적으로 이 프로그램을 기점으로 뢰브너 상은 망했다고 보지만, 다르게 생각하면 **HeX는 제한된 환경에서는 지능적인 것이다**. 그러므로 지능을 이산적으로 이해하려는 시도는 잘못된 것이다. 덜 지능적이거나, 더 지능적일 뿐이다(물론 지능이 한 종류인 것도 아니다).

그러므로 강인공지능에 대비하자는 말에는 주어가 빠져 있다. 이미 우리는 일정 수준의 지능을 가진 인공지능을 매일 쓰고 있으며 그 영향력 안에 들어와 있다. 모두가 위의 애매한 정의를 뚫고 전원 강인공지능이라고 인정할 무언가(를 앞으로는 편의상 강인공지능이라고 말하자)가 나온다면 분명히 그런 인공지능은 인류를 영원히 변화시킬 것이다. 하지만 그 앞에는 수많은 덜 지능적인 인공지능이 존재할 것이고 **그것들의 위험은 강인공지능의 위험과 크게 다르지 않다**. 물론 인간 자신의 삽질로 인한 위험 또한 그 사이에 높아질 것이다. 치명적 위험은 일반적으로 막을 수 있는 것이 아니기에, 꿩 대신 닭이라고 우리가 최우선으로 합의를 봐야 하는 것은 바로 이것이다.

**인공지능을 포함해, 기술의 진보로 인해 닥쳐올 빠른 사회 변화로 인한 구성원의 충격을 최대한 완화하는 방법.**

[Crystal Society](http://j.mearie.org/post/138796860163/crystal-society) 리뷰를 예전에 했었다. 이 소설은 강인공지능이 나오는 소설이지만, 좀 더 정확하게는 강인공지능의 눈으로 바라본 근미래의 인간 사회를 무삭제 노모자이크로 보여 주는 소설이다. 소설에서 각국은 약인공지능으로 인한 사회 변화를 견디지 못 하고 초절정의 삽질을 하고 있다. 현실은 그러지 않길 바란다.

<div class="afternote"><p>이세돌의 4국째 승리와 그 사이에 확인된 다른 정보들을 토대로 약간 수정 가필함. 특히 알파고의 하드웨어 관련된 내용은 언론마다 차이가 심한 편이어서, 그나마 믿을만한 <a href="http://www.economist.com/news/science-and-technology/21694540-win-or-lose-best-five-battle-contest-another-milestone">이코노미스트</a>의 내용을 기준으로 하였다. <small>(2016-03-13)</small></p></div>
