# team8-server

### API 주소
- User

  - /user/register/

    [] POST : 회원가입 및 authtoken 발급

```
request : {
	"email" : "test@test.com",
	"name" : "testUser",
	"password" : "password",
	"student_id": "",
	"college": "",
	"department": "",
	"program": "",
	"academic_year": 1,
	"year_of_entrance": 1
}
response : {
    "email": "myemail2@snu.ac.kr",
	"name": "myname",
	"student_id": "",
	"college": "",
	"department": "",
	"program": "",
	"academic_year": 2,
	"year_of_entrance": 3,
	"token": "eyJ...",
	"refresh_token": "eyJ..."
}
```

  - /user/login/

    [] POST : email, password로 token을 요청

```
request : {
	"email" : "test@test.com",
	"password" : "password"
}
response : {
	"email": "test@test.com",
	"last_login": "2023-01-12 06:52:34.751485+00:00",
	"token": "eyJ...",
	"refresh_token": "eyJ..."
}
```

 - /user/current/

    [] GET : user의 마이페이지 정보를 get

```
request : {}
response : {
	"email": "a@example.com",
	"name": "a",
	"student_id": "",
	"college": "",
	"department": "",
	"program": "",
	"academic_year": 1,
	"year_of_entrance": 1
}
```

- Lecture

  - /lectures/

    [] GET : 강의 list 요청. 가나다순, 10개 기준으로 pagination

```
request : {}
response : {
	"count": 7416,
	"next": "http://ec2-13-125-66-192.ap-northeast-2.compute.amazonaws.com:8000/lectures/?page=2",
	"previous": null,
	"results": [
		{
			"id": 6724,
			"name": "(한)국어교육논문작성의기초",
			"curriculum": "전선",
			"professor": "강효경",
			"department": "국어교육과",
			"number": "M1844.000400",
			"class_number": 1,
			"maximum": 50,
			"cart": 24,
			"current": 24,
			"time": "화(10:00~12:50)",
			"credit": 3,
			"rate": 2.35
		},
	{...}
    ]
}
```

- Lecture 상세검색

  - /lectures?

    [] GET : Body grade, degree, college, department, curriculum, keyword, exception 가능. (모두 선택적 인자)
    - grade: 1, 2, 3, 4, 5
    - degree: 학사, 석사, 박사, 석박사통합, 학석사연계, 학석사통합, 복합학위
    - college: 공과대학, 자연과학대학, ... (수신 사이트 참조)
    - department: 컴퓨터공학부, ...
    - curriculum: 교양, 전필, 전선, ...
    - keyword: 주어진 문자열을 정확히 포함하도록 제한
    - exception: 주어진 문자열을 제외하도록 제한 (여러 개면 comma로 구분)

```
request : {
	"grade" : 2,
	"degree" : "학사",
	"college" : "공과대학",
	"department" : "컴퓨터공학부",
	"curriculum" : "전필",
	"keyword" : "컴퓨터",
	"exception" : "구조"
}
response : {
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2943,
			"name": "컴퓨터프로그래밍",
			"curriculum": "전필",
			"professor": "이영기",
			"department": "컴퓨터공학부",
			"number": "M1522.000600",
			"class_number": 1,
			"maximum": 150,
			"cart": 118,
			"current": 159,
			"time": "화(09:30~10:45)/수(19:00~20:50)/목(09:30~10:45)",
			"credit": 4,
			"rate": null,
			"parsed_time": [
				{
					"day": "TUE",
					"start_time": "09:30:00",
					"end_time": "10:45:00"
				},
				{
					"day": "WED",
					"start_time": "19:00:00",
					"end_time": "20:50:00"
				},
				{
					"day": "THU",
					"start_time": "09:30:00",
					"end_time": "10:45:00"
				}
			]
		}
	]
}
```
    
  - /lectures/<int:id>/

    [] GET : id가 주어진 값인 강의의 detail을 요청.
        (날짜는 ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'] 형태)

```
request : {}
response : {
	"name": "사람 뇌의 구조와 기능",
	"curriculum": "교양",
	"professor": "정천기",
	"department": "의학과",
	"number": "47.019",
	"class_number": 2,
	"maximum": 200,
	"cart": 2,
	"current": 130,
	"time": "",
	"credit": 3,
	"rate": 4.375,
	"parsed_time": [
		{
			"day": "MON",
			"start_time": "18:00:00",
			"end_time": "20:50:00"
		},
		{
			"day": "TUE",
			"start_time": "13:00:00",
			"end_time": "14:50:00"
		}
	]
}
```

- Review

  - /lectures/<int:id>/reviews/

    [] GET : id번 강의 리뷰 리스트를 요청. created_by는 리뷰 생성자가 본인이면 name, 아니면 null

```
request : {}
response : {
	"count": 18,
	"next": "http://ec2-13-125-66-192.ap-northeast-2.compute.amazonaws.com:8000/lectures/1/reviews/?page=2",
	"previous": null,
	"results": [
		{
			"id": 18,
			"title": "1",
			"content": "2",
			"created_by": "test",
			"created_at": "2023-01-04T15:59:10.533384Z",
			"is_updated": false,
			"updated_at": null,
			"rate": 5,
			"course": 1,
			"semester": "4"
	},
	{...}
    ]
}
```

    [] POST : id번 강의에 새 리뷰를 생성
    
```
request : {
	"title" : "review title",
	"content" : "review content",
	"rate" : 3,
	"semester" : "2022-2"
}
response : {
	"id": 14,
	"title": "review title",
	"content": "review content",
	"created_by": "test2",
	"created_at": "2023-01-04T16:04:01.701656Z",
	"is_updated": false,
	"updated_at": null,
	"rate": 3,
	"course": 1,
	"semester": "2022-2"
}
```

  - /lectures/<int:id>/reviews/<int:rid>/
  
    [] GET : id번 강의에 달린 rid번 리뷰의 detail을 요청. rid번 리뷰 생성자/Admin 만 가능. created_by는 리뷰 생성자가 본인이면 name, 아니면 null

```
request : {}
response : {
	"id": 32,
	"title": "review title",
	"content": "review content",
	"created_by": "test2",
	"created_at": "2023-01-04T16:04:01.701656Z",
	"is_updated": false,
	"updated_at": null,
	"rate": 3,
	"course": 1,
	"semester": "2022-2"
}
```

    [] PUT : rid번 리뷰를 수정. rid번 리뷰 생성자/Admin 만 가능

```
request : {
	"title" : "review put",
	"content" : "review content",
	"rate" : 3,
	"semester" : "2022-2"
}
response : {
	"id": 32,
	"title": "review put",
	"content": "review content",
	"created_by": "test2",
	"created_at": "2023-01-04T16:04:01.701656Z",
	"is_updated": true,
	"updated_at": "2023-01-04T16:07:48.215594Z",
	"rate": 3,
	"course": 1,
	"semester": "2022-2"
}
```

    [] PATCH : id번 리뷰를 일부만 수정. id번 리뷰 생성자/Admin 만 가능

```
request : {
    "content" : "review patch",
}
response : {
	"id": 32,
	"title": "review put",
	"content": "review patch",
	"created_by": "test2",
	"created_at": "2023-01-04T16:04:01.701656Z",
	"is_updated": true,
	"updated_at": "2023-01-04T16:09:55.747977Z",
	"rate": 3,
	"course": 1,
	"semester": "2022-2"
}
```

    [] DELETE : id번 리뷰를 제거. id번 리뷰 생성자/Admin 만 가능

```
request : {}
response : 204 No Content
```


- [] Comment

  - /lectures/<int:id>/reviews/<int:rid>/comments/

    [] GET : comment의 리스트를 요청

```
request : {}
response : {
"count": 4,
"next": null,
"previous": null,
"results": [
	{
		"id": 7,
		"created_by": "test2",
		"content": "content",
		"review": 6,
		"created_at": "2023-01-04T10:33:58.767621Z",
		"is_updated": false
	},
   {...}
}
```

    [] POST : 새 comment를 생성
    
```
request : {
	"content" : "content"
}
response : {
	"id": 9,
	"created_by": "test2",
	"content": "content",
	"review": 6,
	"created_at": "2023-01-04T16:14:51.212650Z",
	"is_updated": false
}
```

  - /lectures/<int:id>/reviews/<int:rid>/comments/<int:cid>/

    [] GET : cid번 comment의 detail을 요청

```
request : {}
response : {
	"id": 9,
	"created_by": "test2",
	"content": "content",
	"review": 6,
	"created_at": "2023-01-04T16:14:51.212650Z",
	"is_updated": true,
	"updated_at": "2023-01-04T16:19:37.686856Z"
}
```

    [] PUT : cid번 comment를 수정. cid번 comment 생성자/Admin 만 가능

```
request : {
	"content" : "content put"
}
response : {
	"id": 9,
	"created_by": "test2",
	"content": "content put",
	"review": 6,
	"created_at": "2023-01-04T16:14:51.212650Z",
	"is_updated": true,
	"updated_at": "2023-01-04T16:20:54.072956Z"
}
```

    [] PATCH : cid번 comment를 일부만 수정. pk번 comment 생성자/Admin 만 가능

```
request : {
	"content" : "content patch"
}
response : {
	"id": 9,
	"created_by": "test2",
	"content": "content patch",
	"review": 6,
	"created_at": "2023-01-04T16:14:51.212650Z",
	"is_updated": true,
	"updated_at": "2023-01-04T16:21:18.664607Z"
}
```

    [] DELETE : id가 pk인 comment를 제거. pk번 comment 생성자/Admin 만 가능

```
request : {}
response : 204 No Content
```

- Interest

  - /interest/

    [] GET : header의 토큰 정보를 바탕으로 해당 유저의 관심강좌 목록 조회

```
request : {}
response : {
	"count": 5,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1827,
			"name": "수학연습 2",
			"curriculum": "교양",
			"professor": "서인석",
			"department": "수리과학부",
			"number": "L0442.000400",
			"class_number": 1,
			"maximum": 25,
			"cart": 30,
			"current": 27,
			"time": "금(10:00~11:50)",
			"credit": 1,
			"rate": null,
			"parsed_time": [
				{
					"day": "FRI",
					"start_time": "10:00:00",
					"end_time": "11:50:00"
				}
			]
		},
		{
			"id": 4750,
			"name": "라틴어 1",
			"curriculum": "교양",
			"professor": "양호영",
			"department": "협동과정  서양고전학전공",
			"number": "32.079",
			"class_number": 1,
			"maximum": 40,
			"cart": 87,
			"current": 46,
			"time": "월(15:30~16:45)/수(15:30~16:45)",
			"credit": 3,
			"rate": null,
			"parsed_time": [
				{
					"day": "MON",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				},
				{
					"day": "WED",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				}
			]
		},
		...
	]
}
```

    [] POST : header의 토큰 정보를 바탕으로 해당 유저에게 관심강좌 추가
    
```
request : {
	"number": "32.079",
	"class_number": 1
}
response : {
	"id": 4750,
	"name": "라틴어 1",
	"curriculum": "교양",
	"professor": "양호영",
	"department": "협동과정  서양고전학전공",
	"number": "32.079",
	"class_number": 1,
	"maximum": 40,
	"cart": 87,
	"current": 46,
	"time": "월(15:30\~16:45)/수(15:30\~16:45)",
	"credit": 3,
	"rate": null
}
```

    [] DELETE : header의 토큰 정보를 바탕으로 해당 유저에게서 관심강좌 삭제

```
request : {
	"number": "32.079",
	"class_number": 1
}
response : 204 No Content
```

- Cart

  - /cart/

    [] GET : header의 토큰 정보를 바탕으로 해당 유저의 장바구니 목록 조회

```
request : {}
response : {
	"count": 5,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1827,
			"name": "수학연습 2",
			"curriculum": "교양",
			"professor": "서인석",
			"department": "수리과학부",
			"number": "L0442.000400",
			"class_number": 1,
			"maximum": 25,
			"cart": 30,
			"current": 27,
			"time": "금(10:00~11:50)",
			"credit": 1,
			"rate": null,
			"parsed_time": [
				{
					"day": "FRI",
					"start_time": "10:00:00",
					"end_time": "11:50:00"
				}
			]
		},
		{
			"id": 4750,
			"name": "라틴어 1",
			"curriculum": "교양",
			"professor": "양호영",
			"department": "협동과정  서양고전학전공",
			"number": "32.079",
			"class_number": 1,
			"maximum": 40,
			"cart": 87,
			"current": 46,
			"time": "월(15:30~16:45)/수(15:30~16:45)",
			"credit": 3,
			"rate": null,
			"parsed_time": [
				{
					"day": "MON",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				},
				{
					"day": "WED",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				}
			]
		},
		...
	]
}
```

    [] POST : header의 토큰 정보를 바탕으로 해당 유저에게 장바구니 강좌 추가
    
```
request : {
	"number": "32.079",
	"class_number": 1
}
response : {
	"id": 4750,
	"name": "라틴어 1",
	"curriculum": "교양",
	"professor": "양호영",
	"department": "협동과정  서양고전학전공",
	"number": "32.079",
	"class_number": 1,
	"maximum": 40,
	"cart": 87,
	"current": 46,
	"time": "월(15:30\~16:45)/수(15:30\~16:45)",
	"credit": 3,
	"rate": null
}
```

    [] DELETE : header의 토큰 정보를 바탕으로 해당 유저에게서 장바구니 강좌 삭제

```
request : {
	"number": "32.079",
	"class_number": 1
}
response : 204 No Content
```

- Registered

  - /registered/

    [] GET : header의 토큰 정보를 바탕으로 해당 유저의 수강신청 목록 조회

```
request : {}
response : {
	"count": 5,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1827,
			"name": "수학연습 2",
			"curriculum": "교양",
			"professor": "서인석",
			"department": "수리과학부",
			"number": "L0442.000400",
			"class_number": 1,
			"maximum": 25,
			"cart": 30,
			"current": 27,
			"time": "금(10:00~11:50)",
			"credit": 1,
			"rate": null,
			"parsed_time": [
				{
					"day": "FRI",
					"start_time": "10:00:00",
					"end_time": "11:50:00"
				}
			]
		},
		{
			"id": 4750,
			"name": "라틴어 1",
			"curriculum": "교양",
			"professor": "양호영",
			"department": "협동과정  서양고전학전공",
			"number": "32.079",
			"class_number": 1,
			"maximum": 40,
			"cart": 87,
			"current": 46,
			"time": "월(15:30~16:45)/수(15:30~16:45)",
			"credit": 3,
			"rate": null,
			"parsed_time": [
				{
					"day": "MON",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				},
				{
					"day": "WED",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				}
			]
		},
		...
	]
}
```

    [] POST : header의 토큰 정보를 바탕으로 해당 유저에게 수강신청 강좌 추가
    
```
request : {
	"number": "32.079",
	"class_number": 1
}
response : {
	"id": 4750,
	"name": "라틴어 1",
	"curriculum": "교양",
	"professor": "양호영",
	"department": "협동과정  서양고전학전공",
	"number": "32.079",
	"class_number": 1,
	"maximum": 40,
	"cart": 87,
	"current": 46,
	"time": "월(15:30\~16:45)/수(15:30\~16:45)",
	"credit": 3,
	"rate": null
}
```

    [] DELETE : header의 토큰 정보를 바탕으로 해당 유저에게서 수강신청 강좌 삭제

```
request : {
	"number": "32.079",
	"class_number": 1
}
response : 204 No Content
```

- Timetable
  *현재 num으로 가능한 값은 3, 4, 5
  - /timetable/<int:num>/

    [] GET : header의 토큰 정보를 바탕으로 해당 유저의 num번 시간표의 강좌들을 검색.

```
request : {}
response : {
	"count": 5,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1827,
			"name": "수학연습 2",
			"curriculum": "교양",
			"professor": "서인석",
			"department": "수리과학부",
			"number": "L0442.000400",
			"class_number": 1,
			"maximum": 25,
			"cart": 30,
			"current": 27,
			"time": "금(10:00~11:50)",
			"credit": 1,
			"rate": null,
			"parsed_time": [
				{
					"day": "FRI",
					"start_time": "10:00:00",
					"end_time": "11:50:00"
				}
			]
		},
		{
			"id": 4750,
			"name": "라틴어 1",
			"curriculum": "교양",
			"professor": "양호영",
			"department": "협동과정  서양고전학전공",
			"number": "32.079",
			"class_number": 1,
			"maximum": 40,
			"cart": 87,
			"current": 46,
			"time": "월(15:30~16:45)/수(15:30~16:45)",
			"credit": 3,
			"rate": null,
			"parsed_time": [
				{
					"day": "MON",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				},
				{
					"day": "WED",
					"start_time": "15:30:00",
					"end_time": "16:45:00"
				}
			]
		},
		...
	]
}
```

    [] POST : header의 토큰 정보를 바탕으로 해당 유저의 num번 시간표에 강좌를 추가.
    
```
request : {
	"number": "32.079",
	"class_number": 1
}
response : {
	"id": 4750,
	"name": "라틴어 1",
	"curriculum": "교양",
	"professor": "양호영",
	"department": "협동과정  서양고전학전공",
	"number": "32.079",
	"class_number": 1,
	"maximum": 40,
	"cart": 87,
	"current": 46,
	"time": "월(15:30\~16:45)/수(15:30\~16:45)",
	"credit": 3,
	"rate": null
}
```

    [] DELETE : header의 토큰 정보를 바탕으로 해당 유저의 num번 시간표에서 강좌를 삭제.

```
request : {
	"number": "32.079",
	"class_number": 1
}
response : 204 No Content
```

- 서버 상태

  - GET /state/
  - response
    - period: 서버의 현재 기간
    
| period | 기간        |
|--------|-----------|
| 0      | 수강신청 시작 전 |
| 1      | 장바구니 신청   |
| 2      | 장바구니 확정   |
| 3      | 수강신청      |
| 4      | 개강        |


```
request : {}
response : {
	"period": 1
}
```
