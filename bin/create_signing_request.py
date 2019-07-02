#!/usr/local/bin/python3

# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# AWS Version 4 signing example

import sys, os, base64, datetime, hashlib, hmac 
from datetime import datetime, timedelta
import requests # pip install requests

# ************* REQUEST VALUES *************
method = 'POST'
service = 's3'
host = 'a2c-transcripts-dev-530317771161-s3.s3.amazonaws.com'
region = 'us-west-1'

# Create a date for headers and the credential string
t = datetime.now() + timedelta(hours=9)
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

# Request parameters for CreateTable--passed in a JSON block.
post_policy = '{ "expiration": "'+str(t)+'", "conditions": [ {"acl": "bucket-owner-full-control" }, {"bucket": "a2c-transcripts-dev-530317771161-s3" }, {"x-amz-credential": "AKIAIOCUUZY3CYB4EGUA/20190702/us-east-1/s3/aws4_request" }, {"x-amz-server-side-encryption": "aws:kms"}, {"x-amz-algorithm": "AWS4-HMAC-SHA256"}, {"x-amz-date": "20190702T000000Z"} ] }'

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()


string_to_sign = base64.b64encode(bytes(post_policy,'UTF-8'))

# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.
signing_key = getSignatureKey(secret_key, date_stamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, string_to_sign, hashlib.sha256).hexdigest()

print("Signature = "+signature)
