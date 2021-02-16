# KUBIC Open API 개요
## Open API란 무엇인가?
API란 Application Programming Interface의 준말로 응용 프로그램에서 정보를 전달하고 전달받는 방법을 의미한다. 즉, 프로그램과 프로그램 사이에 정보를 전달할 수 있게 해주는 연결고리의 역할을 한다. API는 공개여부에 따라 비공개 API와 Open API로 나뉜다. 그 중 Open API는 제공자의 기능 또는 콘텐츠를 외부 개발자가 HTTP규약을 통해 호출하여 이용할 수 있도록 한 API를 말한다.  

## KUBIC API의 특징
KUBIC API는 한동대학교 통일빅데이터센터에서 2020년 8월부터 개발된 Open Data API 서비스로, 통일 관련 자료들에 대해 세 가지 데이터 검색(단순 키워드 검색, 상세 검색, 내 보관함 내 검색) 서비스를 제공한다. REST(GET) 방식을 채택하고 있어 사용자가 해당 URI에 대해 GET 요청을 보내오면 요청에 맞는 Json formatted Data를 응답한다. 데이터는 실시간으로 업데이트 된다.  
  
## 서비스 이용 절차
KUBIC Data API를 이용하기 위해서는 활용 신청, 인증, 호출의 세 가지 절차를 거쳐야 한다.  
1.	활용 신청  
활용 신청은 외부 개발자들은 인증키(Service Key 또는 Secret Key)를 제공받고, API제공자는 API이용자들을 관리하기 위해 필요한 절차이다. 본 사이트의 왼쪽 활용 신청 탭에서 사용할 API의 이름과 사용 목적 등을 입력하여 제출 후 신청을 마치면 API는 자동으로 승인이 되며 인증키가 발급된다.  
2.	인증  
인증은 인증키를 이용하여 사용자가 유효한 사용자임을 인증하는 절차이다. API에 요청 메세지를 보낼 때 활용 신청에서 발급된 인증키를 serviceKey 변수에 입력하면 인증이 완료된다.  
3.	호출  
호출은 본격적으로 API에 요청 메세지를 보냄으로써 원하는 응답을 얻어오는 절차이다. 호출할 때에는 요청 URL(Request URL)과 요청 변수(Request Parameter)들를 전송 형식에 맞춰 보낸다. 정해진 형식에 맞추어 응답이 오면 응답을 Parsing하여 이용한다. 이 과정에서는 서비스 상세란에서 상세히 기술된 요청 변수, 응답 변수, 결과 코드를 읽고 적절히 활용하면 된다.

# 서비스 상세
1. 상세 검색
## URL: http:/kubic.org/globalSearch?
## 요청 변수
|변수명(영문)|변수명(국문)|필수 여부|형식|예시|Default값|
|-----------|-----------|---------|----|---|--------|
|serviceKey|인증키|Y|16 bytes String|kvgjI4BaEQ4uDr22xaAIhA|-|
|numOfContents|검색할 최대 개수|N|Int|500|100|
|rank|정렬 기준|N|Int|2(인기순)|1(최신순)|
|keyInTitle|제목 내 검색|Y|String|북핵|-|
|keyInBody|내용 내 검색|N|Int|문재인|-|
|writer|작성자 검색|N|String|홍길동|-|
|startDate|작성일 기간시작점|N|YYYY-MM-DD|2018-09-17|1년 전|-|
|endDate|작성일 기간끝점|N|YYYY-MM-DD|2020-09-17|Today|-|
|institution|발행한 기관명|N|String|북한연구소|-|
|category|분류|N|String|정치|-|

## 요청 예시  
```
전체검색(globalSearch)에서 제목에 ‘북핵’, 내용에 ‘문재인’이 포함되고 2017년과 2020년 사이에 게시된 자료를 찾는 경우>
http://kubic.org/globalSearch?serviceKey=BmBFV2vhwRaiT9&title=북핵&body=문재인&StartDate=20170101&EndDate=20210101
```
  
## 응답 변수  
|변수명(영문)|변수명(국문)|
|-----------|-----------|
|resultCode|결과 코드|
|resultMSG|결과 메세지|
|numOfContents|검색할 최대 개수|
|totalCount|검색된 자료 개수|
|rank|정렬 기준|
|title|제목|
|body|내용|
|writer|작성자|
|date|작성일|
|originalURL|원본 문서 URL|
|institution|발행 기관명|
|institutionURL|발행 기관 URL|
|category|분류|
|fileName|첨부 파일 이름|
|fileURL|첨부 파일 URL|
|fileContent|첨부 파일 내용|


## 응답 예시  
```
{
    "response":{
       "header":{
          "resultCode":"00",
          "resultMSG":"NORMAL_SERVICE"
       },
       "body":{
            "numOfContents":"100",
            "totalCount": "95",
            "rank": "1",
            "contents":[
                {
                    "Title":"북핵에 관하여",
                    "Body":"문재인이 북핵에 관하여 연설했다.",
                    "Writer": "홍길동 기자",
                    "Date":"20200917",
                    "Institution":"북한연구소 본사",
                    "InstitutionURL":"https://BukHan.co.kr",
                    "Category":"정치",
                    "FileURL":"NULL"
                },
			{…},{…}…
            ]
        }
    }
}
```
  
## 활용 예시
### Python

```
import urllib.request as r
import urllib.parse as p
import json
import pandas as pd

url = "http://kubic.org:5000/globalSearch?"
serviceKey = "WF4YJ1-RxrXoiulsWjoLpg"

option = "serviceKey="+serviceKey
request = "&title="+p.quote(title)+"&body="+p.quote(body)
url_full = url + option + request

print("url>"+url_full)
response = r.urlopen(url_full).read().decode('utf-8')
print(response)

jsonArray = json.loads(response) 

if jsonArray.get("response").get("header").get("resultCode") != '200':
    print("Error!!!")
    print(jsonArray.get("header"))
    quit()

    items =jsonArray.get("response").get("body").get("contents")
    print("items>", items)

df = pd.DataFrame(columns=['title','body','writer','date','category','institution','file'])
for item in items:
    df = df.append(item,ignore_index=True)
print(df)
```

## 결과 코드
|결과 코드|결과 메세지|설명|
|--------|----------|----|
|200|OK|요청이 성공적으로 응답되었습니다.|
|204|No Content|요청은 정상적이지만 컨텐츠는 없습니다.|
|400|Bad Request|잘못된 문법으로 인하여 서버가 요청을 이해할 수 없습니다.(파라미터 대소문자 확인 요망)|
|401|Unauthorized|클라이언트가 인증되지 않았습니다.(인증키 확인 요망)|
|502|Bad Gateway|서버가 게이트웨이로부터 잘못된 응답을 수신했습니다.(개발자에게 연락 요망)|

