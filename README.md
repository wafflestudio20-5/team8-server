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

- [] Comment

  - /blog/comments/

    [] GET : comment의 리스트를 요청

       ```
       request : {}
       response : {
       	"count": 4,
       	"next": null,
       	"previous": null,
       	"results": [
    		{
    			"id": 1,
    			"created_by": {
    				"id": 1,
    				"username": "",
    				"email": ""
    			},
    			"content": "",
    			"post": 3
    		},
           ...
       }
       ```

    [] POST : 새 comment를 생성
    
        ```
        request : {
            "content" : "",
	        "post_id" : 3
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

  - /blog/comments/<int:pk>/

    [] GET : id가 pk인 comment의 detail을 요청

        ```
        request : {}
        response : {
        	"id": 1,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "",
        		"email": ""
        	},
        	"created_at": "2022-11-08T06:10:11.607727Z",
        	"updated_at": null,
        	"content": "",
        	"tags": [
                "commenttag1",
                "commenttag2"
            ]
        }
        ```

    [] PUT : id가 pk인 comment를 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [] PATCH : id가 pk인 comment를 일부만 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [] DELETE : id가 pk인 comment를 제거. pk번 comment 생성자/Admin 만 가능

        ```
        request : {}
        response : 204 No Content
        ```

  - [] /blog/posts/<int:post_id>/comments/
    
    [] GET : id가 post_id인 post에 달린 comment의 리스트를 요청.

        ```
        request : {}
        response : {
    	    "count": 2,
	        "next": null,
	        "previous": null,
	        "results": [
	        	{
	        		"id": 15,
	        		"created_by": {
	        			"id": 2,
	        			"username": "testuser2",
	        			"email": ""
	        		},
	        		"content": "",
	        		"post": 14
	        	},
                ...
	        ]
        }
        ```


- [] Comment

  - /blog/comments/

    [] GET : comment의 리스트를 요청

       ```
       request : {}
       response : {
       	"count": 4,
       	"next": null,
       	"previous": null,
       	"results": [
    		{
    			"id": 1,
    			"created_by": {
    				"id": 1,
    				"username": "",
    				"email": ""
    			},
    			"content": "",
    			"post": 3
    		},
           ...
       }
       ```

    [] POST : 새 comment를 생성
    
        ```
        request : {
            "content" : "",
	        "post_id" : 3
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

  - /blog/comments/<int:pk>/

    [] GET : id가 pk인 comment의 detail을 요청

        ```
        request : {}
        response : {
        	"id": 1,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "",
        		"email": ""
        	},
        	"created_at": "2022-11-08T06:10:11.607727Z",
        	"updated_at": null,
        	"content": "",
        	"tags": [
                "commenttag1",
                "commenttag2"
            ]
        }
        ```

    [] PUT : id가 pk인 comment를 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [] PATCH : id가 pk인 comment를 일부만 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [] DELETE : id가 pk인 comment를 제거. pk번 comment 생성자/Admin 만 가능

        ```
        request : {}
        response : 204 No Content
        ```

  - [] /blog/posts/<int:post_id>/comments/
    
    [] GET : id가 post_id인 post에 달린 comment의 리스트를 요청.

        ```
        request : {}
        response : {
    	    "count": 2,
	        "next": null,
	        "previous": null,
	        "results": [
	        	{
	        		"id": 15,
	        		"created_by": {
	        			"id": 2,
	        			"username": "testuser2",
	        			"email": ""
	        		},
	        		"content": "",
	        		"post": 14
	        	},
                ...
	        ]
        }
        ```

- [] Tag

  - /blog/posts/tags/

    [] GET : post에 붙은 태그들의 리스트를 요청

        ```
        request : {}
        response : {
            "count": 3,
	        "next": null,
	        "previous": null,
	        "results": [
	        	{
	        		"content": "tag1"
	        	},
	        	{
	        		"content": "tag2"
	        	},
	        	{
	        		"content": "tag3"
	        	}
	        ]
        }
        ```

  - /blog/posts/tags/<str:tag>/

    [] GET : tag가 태그로 붙은 post의 list를 요청. 생성시간 역순 기준

        ```
        request : {}
        response : {
            "count" : 0,
            "next" : null,
            "previous" : null,
            "results" : [{
	    		    "id": 1,
	    		    "created_by": {
	    		    	"id": 2,
	    		    	"username": "",
	    		    	"email": ""
	    		    },
	    		    "title": "",
	    		    "content": "", // 최대길이 300 제한
	    		    "created_at": "2022-11-08T05:46:37.506875Z"
	    	    },
                ...
            ]
        }
        ```

  - /blog/comments/tags/

    [] GET : comment에 붙은 태그들의 리스트를 요청

        ```
        request : {}
        response : {
        	"count": 2,
        	"next": null,
        	"previous": null,
        	"results": [
        		{
        			"content": "commenttag1"
        		},
        		{
        			"content": "commenttag2"
        		}
        	]
        }
        ```

  - /blog/posts/tags/<str:tag>/

    [] GET : tag가 태그로 붙은 comment의 list를 요청. 생성시간 역순 기준

        ```
        request : {}
        response : {
        	"count": 2,
        	"next": null,
        	"previous": null,
        	"results": [
        		{
        			"id": 1,
        			"created_by": {
        				"id": 1,
        				"username": "",
        				"email": ""
        			},
        			"content": "",
        			"post": 3
        		},
                ...
        	]
        }
        ```

  