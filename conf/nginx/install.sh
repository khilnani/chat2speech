#!/bin/sh -x

cp *.conf  /etc/nginx/conf.d/

service nginx reload
