# -*- coding: utf-8 -*-

import scrapy
from ..items import Item


class NewsSpider(scrapy.Spider):
    name = "news"
    # 삼성전자
    start_urls = [
        "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&oquery=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&tqi=hRk%2B6sp0JXossA4t7VossssstxZ-291757&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&news_office_checked=1011&office_section_code=3&office_type=1&pd=0&photo=0&sort=0"
    ]

    def parse(self, response):
        # 한 페이지 내의 전체 뉴스 url 파싱(페이지당 10개 뉴스)
        news_page_links = response.css('a.news_tit::attr(href)').getall()
        # parse_news 에 위에서 파싱한 url 넘겨주기
        yield from response.follow_all(news_page_links, self.parse_news)
        # 다음 페이지 링크 파싱
        pagination_links = response.css('a.btn_next').attrib['href']
        # 재귀(다음 페이지 파싱)
        yield from response.follow_all(pagination_links, self.parse)

    def parse_news(self, response):
        # 데이터 클렌징
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # 뉴스 정보를 파싱 및 저장

        # 1. scrapy crawl news
        # 문제 : 인코딩 안됨, jl 파일로 저장됨. -> json으로 출력하는 방법 모르겠음
        item = Item()
        item['date'] = extract_with_css('span.url_txt::text').split()[0]
        item['title'] = extract_with_css('div.art_tit::text')
        item['article'] = ''.join(response.css('div.article_view::text').getall()).strip()
        yield item

        # 2. scrapy crawl news -O news.json
        # yield {
        #     'date': extract_with_css('span.url_txt::text').split()[0],
        #     'title': extract_with_css('div.art_tit::text'),
        #     'article': ''.join(response.css('div.article_view::text').getall()).strip(),
        # }