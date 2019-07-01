#!/bin/bash

if [ -d ~/git/a2c/html/css ]; then
  aws --profile nejllreports s3 cp --acl public-read ~/git/a2c/html/css/* s3://a2c-html-530317771161/athlete/css/
fi

if [ -d ~/git/a2c/html/javascript ]; then
  aws --profile nejllreports s3 cp --acl public-read ~/git/a2c/html/javascript/* s3://a2c-html-530317771161/athlete/javascript/
fi
