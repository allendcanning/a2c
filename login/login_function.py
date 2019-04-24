import json
import os, time
import boto3
import hmac
import hashlib
import base64
import time
from jose import jwk, jwt
from jose.utils import base64url_decode
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from botocore.vendored import requests
from urllib.parse import unquote_plus
from urllib.request import urlopen

# Set timezone
os.environ['TZ'] = 'US/Eastern'
time.tzset()

#content_url="https://byh6q12oyj.execute-api.us-east-1.amazonaws.com/dev/"
#s3_html_bucket = "a2c-html-530317771161"
#cognito_pool = "us-east-1_DOD7SyKZu"
#cognito_client_id = "2hfae0s8t0jb0gk1irv27dvsdc"
#cognito_client_secret_hash = "k3uklqp2t5a0dsciq565bfdv1vm6vdq8uiv8n6bn3dh0d22jj3m"

def log_error(msg):
  print(msg)

def get_config_data(environment):
  client = boto3.client('ssm')
  config = {}

  ssmpath="/a2c/"+environment+"/s3_html_bucket"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  config['s3_html_bucket'] = response['Parameter']['Value']
  
  ssmpath="/a2c/"+environment+"/cognito_pool"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  config['cognito_pool'] =response['Parameter']['Value'] 

  ssmpath="/a2c/"+environment+"/cognito_client_id"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  config['cognito_cognito_client_id'] =response['Parameter']['Value'] 

  ssmpath="/a2c/"+environment+"/cognito_client_secret_hash"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  config['cognito_client_secret_hash'] =response['Parameter']['Value'] 

  ssmpath="/a2c/"+environment+"/content_url"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  config['content_url'] =response['Parameter']['Value'] 

  return config

def validate_token(token):
  region = 'us-east-1'
  keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, cognito_pool)
  response = urlopen(keys_url)
  keys = json.loads(response.read())['keys']

  headers = jwt.get_unverified_headers(token)
  kid = headers['kid']
  # search for the kid in the downloaded public keys
  key_index = -1
  for i in range(len(keys)):
      if kid == keys[i]['kid']:
          key_index = i
          break
  if key_index == -1:
      log_error('Public key not found in jwks.json')
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
      log_error('Signature verification failed')
      return False

  # since we passed the verification, we can now safely
  # use the unverified claims
  claims = jwt.get_unverified_claims(token)

  # additionally we can verify the token expiration
  if time.time() > claims['exp']:
      log_error('Token is expired')
      return False

  if claims['aud'] != cognito_client_id:
      log_error('Token claims not valid for this application')
      return False
  return token

def authenticate_user(authparams):
  # Get cognito handle
  cognito = boto3.client('cognito-idp')

  message = authparams['USERNAME'] + cognito_client_id
  dig = hmac.new(key=bytes(cognito_client_secret_hash,'UTF-8'),msg=message.encode('UTF-8'),digestmod=hashlib.sha256).digest()

  authparams['SECRET_HASH'] = base64.b64encode(dig).decode()

  log_error('Auth record = '+json.dumps(authparams))

  # Initiate Authentication
  try:
    response = cognito.admin_initiate_auth(UserPoolId=cognito_pool,
                                 ClientId=cognito_client_id,
                                 AuthFlow='ADMIN_NO_SRP_AUTH',
                                 AuthParameters=authparams)
    log_error(json.dumps(response))
  except:
    return False

  return response['AuthenticationResult']['IdToken']

def print_form():
  content = '<form method="post" action="">'
  content += 'Enter Username: <input type="text" name="username"><p>\n'
  content += 'Enter Password: <input type="password" name="password"><p>\n'
  content += '<input type="submit" name="Submit">'
  content += '</form>'

  return content

def set_portal_data(token,record):
  headers = { 'Authorization': token }

  data = ""
  for item in record:
    data += item+'='+record[item]+'&'

  data = data.rstrip('&')

  r = requests.post(content_url,headers=headers,data=data)

  body = r.text

  return body

def get_portal_data(token,editarea):
  headers = { 'Authorization': token }

  if editarea != False:
    log_error("Calling POST with "+editarea)
    data = "editarea="+editarea
    r = requests.post(content_url,headers=headers,data=data)
  else:
    log_error("Calling GET")
    r = requests.get(content_url,headers=headers)

  body = r.text

  return body

def lambda_handler(event, context):
  token = False
  editarea = False
  record = {}

  log_error("Event = "+json.dumps(event))

  # Build HTML content
  css = '<link rel="stylesheet" href="https://s3.amazonaws.com/'+s3_html_bucket+'/css/a2c.css" type="text/css" />'
  content = "<html><head><title>A2C Portal</title>\n"
  content += css+'</head>'
  content += "<body><h3>A2C Portal</h3>"

  # Get jwt token
  if 'headers' in event:
    if event['headers'] != None:
      if 'Cookie' in event['headers']:
        cookie = event['headers']['Cookie']
        token = cookie.split('=')[1]
        log_error('Got Token = '+token)
        if token != 'False':
          token = validate_token(token)

  if token == False:
    content += print_form()
  elif 'body' in event:
    if event['body'] != None:
      # Parse the post parameters
      postparams = event['body']
      auth = {}
      if '&' in postparams:
        for params in postparams.split('&'):
          key = params.split('=')[0]
          value = params.split('=')[1]
          if key == "Submit":
            continue
          if key == "username":
            auth['USERNAME'] = unquote_plus(value)
          elif key == "password":
            auth['PASSWORD'] = unquote_plus(value)
          elif key == 'editarea':
            editarea = unquote_plus(value)
            record[key] = editarea
          else: 
            record[key] = unquote_plus(value)
      else:
        key = postparams.split('=')[0]
        value = postparams.split('=')[1]
        record[key] = value

      if 'USERNAME' in auth:
        token = authenticate_user(auth)

      if token != False:
        if 'action' in record:
          content += set_portal_data(token,record)
        else:
          content += get_portal_data(token,editarea)
      else:
        content += print_form()
    else:
      content += print_form()
  else:
    content += print_form()

  content += "</body></html>"

  cookie = 'Token='+str(token)
  return { 'statusCode': 200,
           'headers': {
              'Content-type': 'text/html',
              'Set-Cookie': cookie
           },
           'body': content
         }