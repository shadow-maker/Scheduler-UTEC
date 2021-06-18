from app import app

# Deploy config
app_port    =8888
app_debug   =False
app_host    ='127.0.0.1'

# Deploy
app.run(port=app_port, debug=app_debug, host=app_host)
