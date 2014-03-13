SimpleImg
=========

A simple Flask app that allows you to quickly shrink and rotate images for sending via email, txt, or web use

## Install
* Create a content in the same location you put the script and make sure the script can write to it.
* Setup your web server to proxy to the correct port, it defaults to 8001 (Example nginx conf below)
* Run server.py in the background
* Visit site

### Notes
* Nothing cleans up so you could fill your disks space pretty easily
* There are no permissions so if you make it public people would upload what ever they want.

### Example nginx conf
```
server {
    listen 0.0.0.0:80;
    root /var/www/simpleimg.com;
	index index.html;

	server_name simpleimg.com www.simpleimg.com;

    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header HOST $http_host;
        proxy_set_header X-NginX-Proxy true;
        client_max_body_size 10M;
        proxy_pass http://127.0.0.1:8001;
        proxy_redirect off;
    }

    location /js/ {
        autoindex off;
    }
    location /content/ {
        autoindex off;
    }

	error_page 404 /404.html;

	error_page 500 502 503 504 /50x.html;
	location = /50x.html {
	}

	location ~ /\.ht {
		deny all;
    }
}
```
