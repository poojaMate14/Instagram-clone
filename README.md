# Instagram-clone
A basic clone of Instagram app.

A webapp version of the Instagram app where you can:
  - View all posts by all users
  - LogIn, SignUp 
  - Create/Delete a post
  - Create a comment on any post

## TechStack
- Backend: FastAPI
- Database: SQLite
- Frontend: ReactJS

## Snapshots
View all posts and create a comment:  
![image](https://user-images.githubusercontent.com/45240902/211884699-ca3c4bcc-2aa5-449f-b903-4efb98765a31.png)  

Default Screen when logged out:  
![image](https://user-images.githubusercontent.com/45240902/211884175-bb4112ed-c32d-4047-a8fc-3eb517166369.png)  

Login Screen:  
![image](https://user-images.githubusercontent.com/45240902/211884277-ac6fc46e-e79f-47a5-bf57-7a317527d3ef.png)  

SignUp Screen:  
![image](https://user-images.githubusercontent.com/45240902/211884436-e3a8152e-3ebf-4c79-8e37-b519e2eb1e11.png)  


## How to Run
Install all requirements ->
```
pip install -r FASTAPI/requirements.txt
```

FastAPI ->
```
cd FASTAPI/
uvicorn main:app --reload
```

WebUI ->
```
cd WEBAPP/webapp/
npm start
```
