import pandas as pd
import re

def cleansing(text):
    try:
        pattern = "\[.*\]|\s-\s.*" # 대괄호 안에있는 언론사 정보 제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '[0-9]' # 숫자제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '[^\w\s]' # 특수기호제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '([ㄱ-ㅎㅏ-ㅣ]+)' # 한글 자음, 모음 제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '네이버|파이낸셜뉴스|서울경제|이데일리|머니투데이|뉴스|데일리 뉴스|헤럴드 경제|금지|무단|배포|저작권'
        text = re.sub(pattern=pattern, repl='', string=text)
        return text
    except TypeError:
        pass

from konlpy.tag import Komoran
komoran = Komoran(userdic='dic/userdic.txt')
def tokenizing(text):
    try:
        tagged = komoran.pos(text)

        # 일반 명사, 고유 명사, 형용사만 추출
        token = [ word for word,pos in tagged if pos in ['NNG','NNP','VA']]
        return token
    except AttributeError:
        pass

DONGHAK = pd.read_csv('dic/DONGHAK.txt',engine="python",header=None,sep="\t",encoding='cp949')
DONGHAK.columns=['word','sent','score']
DONGHAK=DONGHAK.reset_index(drop=True)
DONGHAK.set_index(['word'],inplace=True)

def pos_scoring(tokens_list):
    try:
        sent_dic = DONGHAK[DONGHAK['sent']=='positive']
        match_word = [x for x in tokens_list if x in sent_dic.index]

        score = len(match_word)

        return score
    except TypeError:
        pass

def neg_scoring(tokens_list):
    try:
        sent_dic = DONGHAK[DONGHAK['sent']=='negative']
        match_word = [x for x in tokens_list if x in sent_dic.index]

        score = len(match_word) * -1

        return score
    except TypeError:
        pass

def tagging(sent):
    try:
        if sent > 0:
            return 1 # 긍정으로 분석된 경우
        elif sent == 0:
            return 0 # 중립으로 분석된 경우
        elif sent < 0:
            return -1 # 부정으로 분석된 경우
    except:
        pass



# test
#text = '상승할 가능성이 높다. 장미빛 미래가 있다. 하락하지 않는다. 하락'
#text = cleansing(text)
#tokens_list = tokenizing(text)
#print('부정 감성 지수',neg_scoring(tokens_list))
#print('긍정 감성 지수', pos_scoring(tokens_list))
#sent  = neg_scoring(tokens_list) + pos_scoring(tokens_list)
#print('종합 분석 의견', tagging(sent))
