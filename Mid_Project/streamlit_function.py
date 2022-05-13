from bs4 import BeautifulSoup
import requests 

import re
from konlpy.tag import Okt

## 크롤링
def headline_scraping(url):   
    url = url

    # 사이트 차단 대비 유저 정보
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

    # soup에 content 담기 
    res = requests.get(url, headers=headers).content
    soup = BeautifulSoup(res, 'html.parser')

    rate = "정보없음"

    try: 
        if ('sports' in url) and ('naver' in url): 
            headline = soup.find('h4', {'class':'title'}).get_text()
        elif 'naver' in url:
            headline = soup.find('h2', {'class':'media_end_head_headline'}).get_text()
        elif 'daum' in url: 
            headline = soup.find('h3', {'class':'tit_view'}).get_text()
    except:
        return rate

    return headline


## 전처리
# 한자 등 텍스트 대치 함수
def preprocessing(text):
    # 개행문자 제거
    text = re.sub('\n', ' ', text)
      # 일부 한자 수정 
    name = {'↑':"상승",'↓':"하락",'㈜':"","銀":"은행","外人":"외국인",
            "日":"일본","美":"미국","北":"북한","英":"영국","中":"중국","與":"여당","靑":"청와대","野":"야당","伊":"이탈리아",
            "韓":"한국","南":"한국","獨":"독일","佛":"프랑스","檢":"검찰","銀":"은행","亞":"아시아","人":"사람","企":"기업",
            "前":"이전","車":"자동차","軍":"군대","19":"코로나", "朴":"박근혜", "文":"문재인", "安":"안철수", "展":"전시회", 
            "反":"반대", "故":"사망", "男":"남자", "女" : "여자", "硏":"연구", "코로나 19":"코로나19"}
    for i, j in name.items():
        text = text.replace(i, j)
    # 한글, 영문만 남기고 모두 제거
    text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z]', ' ', text)  # 숫자나 한자(一-龥)는 모델 적용한 뒤 성능을 비교해 보고 다시 작성
    # 중복으로 생성된 공백값을 제거 
    text = re.sub('[\s]+', ' ', text)
    # 영문자를 소문자로
    text = text.lower()
    return text

def make_corpus(sentence):
    
    sentence = preprocessing(sentence)
    
    # 많이 나오지만 분석에 도움이 되지 않는 단어들 제거
    # 한 글자 단어 중 의미있는 단어는 포함하고 나머지는 제외
    del_list = ['같다','모든','하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다',
               '우리','저자','통해','무엇','대한','대해','위해','또한','이야기','지금','모두','리즘','모습','먼저','이제','제대로',
               '얼마나','바로','이후','여러','누구','불구','동안','크게','서도','감히','로서','달리','만큼','비롯','매우','가까이',
               '미리','어쩌면','면서','더구나','오히려','게다가','관련','어디','역시','더욱','여기','저기','거기','결코','거나','앞서',
               '마치','경우','사이','종합','한국','내년','없다','내달','올해','앞두다','코로나'] + ['평','뇨','뤽','옵','며','꽤','록','주','봇','타','림','녀','펑','테', '단','겸','캡','압','좀','맏','텔','뽕','곤',
                '빠','자','현','판','납','댓','완','녜','준','푼','렉','샷','데','액','옐','텐','깃','곁','볼','바','옥','백','뿐','학','웅','실','호','갠','장','빵','숱','냐','윤',
                 '엔','즐','헛','샛','릴','관','밀','삼','융','결','맘','딜','낼','럼','승','벨','안','북','역','피','니','숄','텅','꽉','콘','탓','캣','초','겨','갱','얍','답','폴','및','하','용','붐',
                 '건','뭐','톰','닛','란','새','석','딸','보','삑','펀','낚','퇴','딕','윌','과','죽','킴','옆','이','낙','십','궤','쿵','분','일','남',
                 '욱','상','퀀','팬','젭','룬','숨','회','탕','캔','펠','토','둘','멸','트','팔','거','워','밸','곳','칩','컴','터','뼈','특','국','웡','펜','울','충','뮤','펄','쇄','계','령','신','별','덤','염','린','엽','숍','콕','색','번','육','확','넷','무','퍼','쾅','후',
                 '필','런','셧','제','잡','온','탭','꺽','팸','닷','킷','기','절','탈','핵','맹','툭','옻','삭','비','전','몽','톡','슈','았','앤','읍','엮','쿨','헬','왜','익','렬','털','각','블','획','첫','폭',
                 '처','짓','면','잭','사','치','빅','민','룸','걸','작','깅','만','왕','빙','님','칠','쑹','닥','수','뭘','덴','료','훙','녹','악','횡','앱','접','줌','여','숭','팩','뒤','랜','퓌','누','등','쉬','를','륙','포','쟁','협','저','홍','또','성','뼘','암','쇠','티','던',
                 '환','페','떼','샹','밍','더','옷','직','슨','벼','카','쿠','멈','청','힙','질','팽','마','명','증','랬','맥','탁','숙','박','취','쇤','캐','궂','움','콩','롱','핫','늘','략','원','귀','즈','키','죄','로','조','챙','롭','함','활','삶','좌','윈','측','몬','다','낭','정','넛','팝',
                 '의','즘','컷','램','변','핏','틴','줄','체','엄','간','루','켜','롬','행','규','셈','척','매','띤','슝','그','멍','딥','킥','음','놀','삐','푹','곡','솔','빼','권',
                 '르','세','위','홈','길','쥴','엡','립','외','빈','몇','머','툰','채','락','류','혁','베','나','능','뻔','슛','진','앰','식','컬','룽','족','끗','찬','켄','레','웨','곽','땐','쩐','김','헤','노','량','펩','둥','틀','황','쌍','응','메','텄','맨','디','텍','뱅','봉','송','넉','년','웰','알','룰','갓',
                 '속','펍','편','론','찌','쉑','친','휑','감','은','례','뎅','빔','태','렌','젬','짤','셀','틈','핸','칸','덜','득','몫','윅','널','짐','징','병','임','종','앗','냥','템','살','고','늦','양','뎀','솎','젤','랩','닉','릿','난','쯤','중','큐','날','링','두','소','콜','뼛','리','썸',
                 '항','짊','점','요','셰','킹','재','스','낮','픽','껜','툴','샵','룡','률','쏠','쉰','훈','묵','듯','힐','엘','순','시','윙','꿴','동','킨','러','롯','롤','혼','얀','붕','퐁','델','팀','잔','륭','킬','샘','선','경','내','심','슬','벌','놈','얼','추','객','택','욕','겹','즌','뻥','엠','웬','댕','츠','프','팅',
                 '오','적','덕','끌','억', '업','맵','늪','인','막','케','퀸','유','흑','브','턴','존','람','쉘','쓱','셋','섭','헌','파','휘','톤','입','효','설','월','낫','패','쾌','연','랄','팁','운','냉','샤','앞','착','도','쿡','캉','애','합','투','쭉','을','찍','버','생','뷰','휠','쪽','뚜','덧','싹','해','모','예','홀','드','젠','칙','부','에','잼',
                 '몹','와','션','웃','최','열','혜','어','교','캠','불','궐','는','영','망','빨','너','것','네','려','율','쏙','맷','구','쩍']   
    
    # kernel dead가 뜨면 이모티콘 제거 해야함
    tokenizer = Okt()
    raw_pos_tagged = tokenizer.pos(sentence, norm=True, stem=True) # POS Tagging
    word_cleaned = []
    
    # 명사, 형용사, 동사, 영단어만 포함 
    for word in raw_pos_tagged: #  ('서울', 'Noun'),
        if word[1] in ['Noun','Alpha','Adjective','Verb']: # Foreign ==", " 와 같이 제외되어야할 항목들
            if word[0] not in del_list: # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
                word_cleaned.append(word[0])

    return ' '.join(word_cleaned)


## 모델은 따로 pickle  형태로 저장 (pkl)해서 불러오기 
## --> 일단 임의로 linear svc 만들기 
## --> 일단 임의로 tf-idf 만들기 

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


def model(text):
    text = [text]
    topic = ['IT과학', '경제', '사회', '생활문화','세계','스포츠','정치']
    loaded_tf = joblib.load('./tf_idf.pkl')
    loaded_model = joblib.load('./svc_model.pkl')

    tf_text = loaded_tf.transform(text)
    pred = loaded_model.predict(tf_text)

    return topic[int(pred)]