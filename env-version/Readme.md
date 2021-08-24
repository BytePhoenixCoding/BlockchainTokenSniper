This bot working for runing in the cloud service that needed the .env, variable instead put sensitive data in config.json which is risky if you run in the cloud service.
Tested at replit. it's mean posible to run script in heroku or alternative service.

![replit](https://user-images.githubusercontent.com/16743443/130622003-5cf0251a-df38-415a-b8d8-fcdb6d979322.PNG)

if you find error when runing, please change the os.environ with .env support like os.getenv or anything else.
