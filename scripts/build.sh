#!/bin/bash

aws --profile nejllreports s3 cp --acl public-read ~/git/a2c/html/css/* s3://a2c-html-530317771161/css/
