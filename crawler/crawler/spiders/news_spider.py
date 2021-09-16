import scrapy


class NewsSpider(scrapy.Spider):
    # 스크래피에서 스파이더는 어디에서 어떤 데이터를 수집했는지 정의하는 구간
    name = "news"
    # 네임은 스파이터 이름이다. 이름을 바꿔주면 < crawl 이름 > 이라는 명령어로 실행할 수 있음
    # 아래는 네이버 뉴스 검색 - 검색어 : 삼성전자 / 신문사 : 서울경제
    start_urls = [
        'https://search.naver.com/search.naver?where=news\
        &sm=tab_pge&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90\
        &sort=2&photo=0&field=0&pd=0&ds=&de=&mynews=1&office_type=1\
        &office_section_code=3&news_office_checked=1011&nso=so:r,p:all,a:all&start=1'
    ]

    def parse(self, response):
        # 한 페이지 내의 전체 뉴스 url 파싱(페이지당 10개 뉴스)
        news_page_links = response.css('a.news_tit::attr(href)').getall()
        # parse_news 에 위에서 파싱한 url 넘겨주기
        yield from response.follow_all(news_page_links, self.parse_news)
        # a.btn_next
        # 다음 페이지 링크 파싱
        pagination_links = response.css('a.btn_next:attr(href)').get()
        # 재귀(다음 페이지 파싱)
        yield from response.follow_all(pagination_links, self.parse)

    def parse_news(self, response):
        # 데이터 클렌징
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # 뉴스 정보를 파싱 및 저장
        '''
        해야 할 일:
        1. fake_useragent 설정 **middlewares**
        2. 아래 코드를 yield 말고, 저장(json, csv...etc)으로 바꾸기
        Q. 이 과정을 **piplelines.py**에서 진행할 수 있을까?
        '''
        yield {
            'date': extract_with_css('span.t11::text').get(),
            'title': extract_with_css('h3.tts_head::text'),
            'article': extract_with_css('div._article_body_contents::text')
        }
