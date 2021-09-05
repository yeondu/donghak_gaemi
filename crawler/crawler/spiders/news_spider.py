import scrapy


class NewsSpider(scrapy.Spider):
    # 스크래피에서 스파이더는 어디에서 어떤 데이터를 수집했는지 정의하는 구간
    name = "news"
    # 네임은 스파이터 이름이다. 이름을 바꿔주면 < crawl 이름 > 이라는 명령어로 실행할 수 있음
    def start_requests(self):
        # start_request는 어떤 웹사이트에서 데이터를 수집할건지 정의
        urls = [
            'https://www.sedaily.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # parse메서드는 이 웹사이트를 통해서 반환된 응답 중 어떤 데이터를 수집할지 정의하는 구간
        # response.css() 매서드나 response.xpath() 메서드를 통해 원하는 값을 가져올 수 있음.
        # 사이트.robot.txt 네이버에서 크롤링하지말라고 정책이되어있기 때문에 settings.py 에서 ROBOTSTxT_OBY
        #를 FALSE로  변경하면 정책이 무시가되고 실행할 수 있다.
