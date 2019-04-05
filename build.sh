#!/bin/bash

cd package
zip -r9 ../a2c.zip .
cd ../
zip -g a2c.zip buildspec.yml *.py samTemplate.yaml

