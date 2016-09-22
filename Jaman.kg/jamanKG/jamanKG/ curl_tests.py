
"""
    $ curl -X POST -d "username=kolokol&password=kolokol123" http://127.0.0.1:8000/api/auth/token/

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InByb2YiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6IiIsImV4cCI6MTQ3MzU3MTI5Mn0.vf3yGbT4M4Rut8LskimSYhMTH4tdbAAgKeRmGvSfXFs
    
    curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InByb2YiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6IiIsImV4cCI6MTQ3MzU3MTI5Mn0.vf3yGbT4M4Rut8LskimSYhMTH4tdbAAgKeRmGvSfXFs
" http://127.0.0.1:8000/api/comments/
     
     curl -X POST -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImtvbG9rb2wiLCJ1c2VyX2lkIjoxMywiZW1haWwiOiJrb2xva29sQG1haWwucnUiLCJleHAiOjE0NzM1NzM5NzJ9.6RBC6gjcpdk6IW95GFXXMKc4tdBzHmOreNSJEnugU-E" -H "Content-Type: application/json" -d '{"content":" Yeap we are on finish line"}' 'http://127.0.0.1:8000/api/comments/create/?type=post&slug=maria-rya&parent_id=8'
    
    curl  http://127.0.0.1:8000/api/comments/


"""