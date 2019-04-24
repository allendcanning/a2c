# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

from urllib.request import urlopen
import json
import time
from jose import jwk, jwt
from jose.utils import base64url_decode

region = 'us-east-1'
userpool_id = 'us-east-1_DOD7SyKZu'
app_client_id = '2hfae0s8t0jb0gk1irv27dvsdc'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
response = urlopen(keys_url)
keys = json.loads(response.read())['keys']

def lambda_handler(event, context):
    token = event['token']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    print(claims)
    return claims
        
# the following is useful to make this script executable in both
# AWS Lambda and any other local environments
if __name__ == '__main__':
    # for testing locally you can enter the JWT ID Token here
    event = {'token': 'eyJraWQiOiI2cEtUbGEwdll5TnoxZHp5ck11RUtUOUl5NjhIaDFnaVdiTEdCZ2kxak5NPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzYzllZjUyZi00Y2U4LTQ1MDMtYjI5OS0wMDAxMTU5ZjA5YTEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfRE9EN1N5S1p1IiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJjb2duaXRvOnVzZXJuYW1lIjoiY2FubmluZyIsImF1ZCI6IjJoZmFlMHM4dDBqYjBnazFpcnYyN2R2c2RjIiwiZXZlbnRfaWQiOiJjMTM2N2U0YS02NWU5LTExZTktYjJiMC0yZDVmYTU0NDczMzMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTU1NjAzOTAyNSwicGhvbmVfbnVtYmVyIjoiKzE1MDg5ODI2ODQ0IiwiZXhwIjoxNTU2MDQyNjI1LCJpYXQiOjE1NTYwMzkwMjUsImVtYWlsIjoiY2FubmluZ0BjYW5uaW5nYnJhbmNoLmNvbSJ9.XWy_TLVSgJMpBZ_9lR4E62CxfDD_iVuxzONwfj7ONhg4It0QP8xdfD4vAat-Jhg6EfWk1_cxTElBAVDRNVJ77ETL1omMe2lWhpZqWtZ1mHSAy-pTQhi0PoKrZ_MO5XGJM1babuXaDOQ5GteVdLASRxgGFRDPIn6OqKvX60mjz0C8KBi4HiC84-ZXSP3ylA641Fiwoo9mRR_xCo0Sc7Juyq0VATS0cNkofs9cE8FxWl1c4yNXYxdgsX9WDTkzeFzeFA22dNmfHcFTlajBMDCPGr4uuQbYr29p-ij0KqUfU5QoEWKtRXQiWvtNOssYxz-SLzrQmEqGRxI-Cu8KdPfuig'}
    lambda_handler(event, None)
