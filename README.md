# Donghak_gaemi
빅데이터 기반 주식 및 뉴스 분석 시스템 구축
웹페이지 구축

## Description


## 웹페이지 구축
- Django 사용

```python
{% block content %}

{% endblock %}
```
- 기본 바탕이 되는 base.html을 생성후 변동되는 부분만 `{% block content %}` 으로 감싸주어 해당 부분만 각 페이지에 맞게 변경

```python
{% extends 'base.html' %}
{% block content %}
{% endblock %}
```
- 변경할 html에서 `{% extends 'base.html' %}`코드를 사용해 base.html을 기본 바탕으로 사용
- 변경되는 내용은 base.html과 동일하게 `{% block content %}` 안에 작성

### 시작페이지(종목 나열, ai 분석 결과)

![gaemis](https://user-images.githubusercontent.com/80117053/149608091-2b13b036-3aa3-4fa9-9cab-77258a50e162.png)

1. 변수 전달(데이터 전달)

`views.py`
```python 
def home(request):
    MAX_LIST_CNT = 10 # 한 페이지에 보여주는 종목 수
    name = stockModel.objects.values('stock_name')
    r = []
    for n in name: # 주식 리스트 생성
        code = stockModel.objects.filter(stock_name=n['stock_name']).values('stock_code')[0]
        price_id = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('stock_id')[0] # 주가 아이디
        close = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[0]
        before = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[1]
        fluc = round(((close['close'] - before['close'])/close['close']), 2)
        fluction = {'fluction':fluc}
        predict = predictModel.objects.filter(stock_id = price_id['stock_id']).values('result')[0]
        accuracy = accuracyModel.objects.filter(stock_code = code['stock_code']).order_by('-model_id').values('accuracy')[0]
        result = {**n, **code, **close, **predict, **accuracy, **price_id, **fluction}
        r.append(result)
```
- Django에서 데이터 형태는 json이기에 전달되는 변수의 데이터 형태도 json 형태여야 한다
- 하지만 여러 데이터베이스에서 정보를 추출하고 통합하여 전달하는데 있어 단순 쿼리로는 한계가 있어 각 데이터들을 딕셔너리 형태로 만들어 전달해야 한다
- list.html에서 반복문을 활용하여 테이블을 생성하기에 각 정보들을 딕셔너리로 만들어 더 큰 딕셔너리 하나로 묶어 전달
- 인덱스를 활용한 쿼리는 json로 결과가 제공된다. 해당 정보들을 한 딕셔너리로 묶기 위해 {**data1, **data2}를 사용해 하나의 객체를 생성, 전달


`list.html`
```python
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>

            {% for list in page %}
                    <tr class = "text-center">
                        <td><a href = "detail/{{ list.stock_id }}" style = 'color:black'>{{ list.stock_name }}</a></td> <!-- 종목명 -->
                        <td>{{ list.stock_code }}</td> <!-- 종목코드 -->
                        <td>{{ list.close }}</td> <!-- 가격 -->
                        {% if list.fluction > 0 %}
                            <td id = up>{{ list.fluction }}%</td> <!-- 등락률 -->
                        {% elif list.fluction <= 0 %}
                            <td id = down>{{ list.fluction }}%</td>
                        {% endif %}
                        {% if list.result == 1 %}
                            <td><button class = "btn btn-light">상승</button></td> <!-- 상승/하락 예측 -->
                            <td id = up>{{ list.accuracy }}%</td> <!-- 확률 -->
                        {% elif list.result == 0 %}
                            <td><button class="btn btn-primary" style = "border-radius: 30px; ">하락</button></td>
                            <td id = down>{{ list.accuracy }}%</td> <!-- 확률 -->
                        {% endif %}

                    </tr>
            {% endfor %}
```

- bootstrap 라이브러리를 사용해 html 디자인
- 등락률: 전날 종목 가격과 오늘날 종목 가격의 비율
- 상승/하락 예측: ai 분석을 통한 상승/하락 예측
- 확률: ai 분석이 예측한 상승/하락 확률(정확도)
- for문을 활용하여 반복적으로 행 생성
- {{변수.딕셔너리키}} 형태로 적어 각 딕셔너리키에 대한 딕셔너리값을 불러옴

2. 페이징처리

`views.py`
```python 
from django.core.paginator import Paginator

def home(request):
    MAX_LIST_CNT = 10 # 한 페이지에 보여주는 종목 수
    name = stockModel.objects.values('stock_name')
    r = []
    for n in name: # 주식 리스트 생성
        code = stockModel.objects.filter(stock_name=n['stock_name']).values('stock_code')[0]
        price_id = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('stock_id')[0] # 주가 아이디
        close = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[0]
        before = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[1]
        fluc = round(((close['close'] - before['close'])/close['close']), 2)
        fluction = {'fluction':fluc}
        predict = predictModel.objects.filter(stock_id = price_id['stock_id']).values('result')[0]
        accuracy = accuracyModel.objects.filter(stock_code = code['stock_code']).order_by('-model_id').values('accuracy')[0]
        result = {**n, **code, **close, **predict, **accuracy, **price_id, **fluction}
        r.append(result)

    page = request.GET.get('page', 1)  # page 번호를 get 파라미터로 받고 없으면 기본값 1로 설정
    list = r
    paginator = Paginator(list, MAX_LIST_CNT)
    page_obj = paginator.get_page(page)
    context = {'page': page_obj}
    return render(request, 'stock/list.html', context)
```
- 페이징처리를 위해 Paginator 패키지 사용
- page로 page 번호를 인수로 받고 해당 page에 대한 정보 얻음
- paginator로 해당 page에 들어갈 정보와 한 페이지에 들어갈 최대 종목 수를 정해 넣는다. 
- page_obj에 page 번호에 대한 페이지 정보를 객체로 저장하여 전달

`list.html`
```python
<!--페이지리스트-->
    <div class = "row">
        <ul class = "pagination justify-content-center">
            {% for page_number in page.paginator.page_range %}
            {% if page_number == page.number %}
            <li class = "page-item active" aria-current="page">
                <a class = "page-link" href = ?page={{ page_number }}>{{ page_number }}</a>
            </li>
            {% else %}
            <li class = "page-item">
                <a class = "page-link" href = "?page={{ page_number }}">{{ page_number }}</a>
            </li>
            {% endif %}
            {% endfor %}

        </ul>
    </div>
```
- for문과 if문을 통해 전체 페이지 리스트 중 현재 페이지 넘버와 반복되는 전체 페이지 리스트와 일치하면 해당 페이지 링크는 파란색으로 현재 위치라고 표시되고 그렇지 않은 페이지 번호들은 기존 상태를 유지한다. 



### 감성분석 페이지

![스크린샷(206)](https://user-images.githubusercontent.com/80117053/149610964-73e02017-2bbf-44fb-b60b-fd6b314c2e25.png)

1. 가격 차트 생성

`views.py`
```python 
    price = priceModel.objects.filter(stock_code = close.stock_code).order_by('date')
    chart_list = []
    close_list = []
    for p in price:
        time_tuple = strptime(str(p.date), '%Y-%m-%d')
        utc_now = mktime(time_tuple) * 1000
        chart_list.append([utc_now, p.open, p.high, p.low, p.close])
        close_list.append(p.close)
    
    price = {'close':close,
             'difference':difference,
             'fluction':fluction,
             'stock':stock,
             'close_list':json.dumps(close_list),
             'chart_list':json.dumps(chart_list),
             'page':page_obj}
    return render(request, 'stock/detail.html', price)
```
> 여기서 주의할점은 날짜(date)인데 2010-12-11이라는 datetime형태가 아닌 utc형
(1540000231)으로 변환해주어야 나중에 highstock에서 제대로 된 시간축(x축)을 만들
수 있다 .
- chart에 들어갈 가격과 날짜 정보를 list 형태로 저장. 이때, 날짜의 형태는 datetime에서 utc형태로 변환해준다. 
- 모든 데이터는 json 형태여야 하므로 json.dumps를 사용하여 리스트를 json 형태로 변환하여 전달

`detail.html`
```python
<div id = "container" style = "margin:100px;">

    <script src = "https://code.highcharts.com/stock/highstock.js"></script>
    <script src = "https://code.jquery.com/jquery-3.3.1.min.js"></script>
        <script>
            function setChart() {
            Highcharts.setOption({
                global: {
                    useUTC: false
                }
            });
        };
            Highcharts.stockChart('container', {


        rangeSelector: {
            selected: 1
        },

        title: {
            text: ''
        },

        series: [{
            type: 'candlestick',
            name: '',
            data: {{ chart_list }}
        }]
    });
        </script>
</div>
```

- jquery와 Highcharts에서 highstock을 사용하여 차트 생성
- rangeselector: 표시할 날짜 범위 선택. selected:1으로 하면 기본 3개월 차트를 보여준다


2. 뉴스 카드 생성(페이징 처리는 위 시작 페이지와 동일, 단 6개의 뉴스를 한 페이지에 보여줌)

`views.py`
```python 
def detail_stock_news(request, id):
    close = priceModel.objects.get(stock_id = id)
    news_id = newsModel.objects.filter(stock_code = close.stock_code).order_by('-registration_date').values('news_id')
    news_list = []
    for n in news_id:
        news_press = newsModel.objects.filter(news_id = n['news_id']).values('press')[0]
        news_link = newsModel.objects.filter(news_id = n['news_id']).values('link')[0]
        news_title = newsModel.objects.filter(news_id = n['news_id']).values('title')[0]
        result = sentimentModel.objects.filter(news_id = n['news_id']).values('result')[0]
        list = {**news_press, **news_link, **news_title, **result}
        news_list.append(list)
```
- id 인수를 통해 stock_id를 전달받아 사용
- 위 시작 페이지와 동일하게 각 데이터베이스로부터 데이터를 추출해 하나의 객체로 통합해 전달
- 해당 종목에 대한 뉴스, 각 뉴스 별 감성분석 결과, 링크를 전달 해당 뉴스 원문으로 이동

`detail.html`
```python
<div class = "row" >
            <!-- 감성분석 결과 -->
            <h3 style = "margin: 0px 0px 20px 120px">분석결과</h3>
            <div class = "col" style = "margin:0px 0px 20px 120px">
                <button class = "btn btn-primary" style = "border-radius: 30px;" >감성분석</button>
                <button class = "btn btn-light" style = "border-radius: 30px;"><a href = "ai/{{ close.stock_id }}">AI분석</a></button>
            </div>
        </div>

        <div class = "row" style = "margin-left:120px">
            <!-- 뉴스 카드 -->
            <h3> 뉴스 </h3>
        </div>
    <div class = "container" >
        <div class = "row">
            {% for n in page %}
                <div class = "col-sm-3" style="margin:25px;">
                    <div class = "card text-center" style = "border-radius: 30px;">
                        <div class = "card-header" style = "text-align:center">
                            {{ n.press }}
                        </div>
                        <div class = "card-body">
                            <a class = "card-text" href = {{ n.link }}>{{ n.title }}</a></br>
                            {% if n.result  == 1 %}
                                <button class = "btn btn-light" style = "background-color:rgba(250, 166, 176, 1);
border-radius:30px;">상승</button>
                            {% else %}
                                <button class = "btn btn-primary">하락</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% if forloop.counter|divisibleby:"3" and not forloop.last %}
                </div><div class = "row">
                {% endif %}
            {% endfor %}
        </div>
```
- class card를 사용하여 뉴스를 카드 형태로 생성
- 뉴스 제목에 링크를 달아 제목을 클릭 시 해당 뉴스 원문으로 이동
- `{%if forloop.counter}`를 사용하여 한 줄에 3개씩 총 2줄 형태로 나오도록 함
- 화면 크기 상 개수를 더 늘이면 화면 옆쪽으로 넘어감



### ai 분석 페이지

![스크린샷(207)](https://user-images.githubusercontent.com/80117053/149611449-7041144f-3ae2-4fff-afa1-0c3dc16a1cae.png)

- 해당 종목에 대한 가격, 등락률, 가격차트 시각화
- 해당 종목에 대한 90일 후 예측 결과, 예측 확률

`urls.py`
```python
urlpatterns = [
    path('detail/ai/<int:id>', views.detail_ai, name = 'detail_ai'),
]
```
- url 설정에서 ai 분석 페이지로 간 후 이전 페이지로 돌아가거나 다른 페이지로 넘어가는 url로 생성하지 못함(보완 필요)


