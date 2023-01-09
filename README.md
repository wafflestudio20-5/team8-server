# team8-server

### API 주소
- User

  - /user/register/

    [] POST : 회원가입 및 authtoken 발급

        ```
        request : {
    	    "email" : "test@test.com",
    	    "name" : "testUser",
    	    "password" : "password"
        }
        response : {
            "email": "test@test.com",
	        "name": "testUser",
            "Token" : "eyJ..."
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
    	    "last_login": "2023-01-04 15:29:53.282981+00:00",
    	    "token": "eyJ..."
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
