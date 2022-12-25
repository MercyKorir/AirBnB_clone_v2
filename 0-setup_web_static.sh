#!/usr/bin/env bash
#This script sets up web servers
#for the deployment of web-static

apt-get install -y nginx
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Alx is Amazing" >> /data/web_static/releases/test/index.html
ln -s -Ff /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served-By $HOSTNAME;

	root /var/www/html;
	index index.html;

	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html;
	}
}"
service nginx restart
