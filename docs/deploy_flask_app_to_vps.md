# Deploy Flask app  to VPS with NGINX

## NGINX Configuration : 
Under '**_/etc/nginx/conf.d/server.conf_**' add flask app location : 
```
location /pc-builder-app/ {
        proxy_pass             http://127.0.0.1:5001;
        proxy_read_timeout     60;
        proxy_connect_timeout  60;
        proxy_redirect         off;

        # Allow the use of websockets
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
   }
```
In this demo we are using '**/pc-builder-app/**' as subdomain

## Docker Configuration : 
In the docker-compose file, Add Domain and Environment to the flask app environment variables running with docker : 

```
services:
  pc-builder-app:
    container_name: pc-builder-app
    ...
    environment:
      - DOMAIN=/pc-builder-app
      - ENV=PROD
    ...
```

## Flask app configuration : 
- In app.py (main.py) : 
<br>

Implement Flask Blueprint to add app domain/subdomain to all application routes, templates and static files.

```
from flask import Flask, Blueprint

# Import of environment variables
environment = os.environ['ENV']
app_domain = os.environ['DOMAIN'] if environment == 'PROD' else ''

app_bp = Blueprint('app_bp', __name__,
    template_folder='templates',
    static_folder='static')

# Apply Bluprint 'app_bp' to route
@app_bp.route('/')
def home():
    return render_template('index.html', app_domain=app_domain)

# Apply Blueprint with url_prefix in production mode after all routes
if environment == "PROD":
    app.register_blueprint(app_bp, url_prefix=app_domain)
else:
    app.register_blueprint(app_bp)

if __name__ == "__main__":
...
```
- In template files : 
<br>

1 - Pass app_domain to route props : 

```
app_domain = os.environ['DOMAIN'] if environment == 'PROD' else ''

@app_bp.route('/')
def home():
    return render_template('index.html', app_domain=app_domain)
```

2 - Add app_domain to css link stylesheet, js script, images and a tag href : 

```
<script src="..{{ app_domain }}/static/js/main.js"></script>

<link rel="stylesheet" href="..{{ app_domain }}/static/css/main.css" />

<img src="..{{ app_domain }}/static/images/ccmainbanner-1.jpg" alt="" />

# link to main.html (/main)
<a class="btn btn-success" href="{{ url_for('app_bp.main') }}">Build your own PC</a>
```

- In JS files :
<br> 

1 - Pass app_domain (eg : main.html)  with the script tag : 

```
<script>var appDomain = "{{ app_domain }}";</script>
```

2 - consume app_domain in dedicated JS file (eg : main.js) : 

```
window.document.location = appDomain + "/order";
```