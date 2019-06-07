#!/usr/local/bin/python3

import json
from optparse import OptionParser
import boto3
from botocore.exceptions import ClientError

client = boto3.client('ssm')

# Functions used
def Usage():
  parser.print_help()

def log_error(msg):
    print(msg)

def get_client_secret(session,pool,id):
  client = session.client('ssm')
  environment = "dev"

  ssmpath="/a2c/"+environment+"/"+id+"_cognito_client_id"
  response = client.get_parameter(Name=ssmpath,WithDecryption=False)
  clientid = response['Parameter']['Value']

  client = session.client('cognito-idp')
  try:
    response = client.describe_user_pool_client(
      UserPoolId=pool,
      ClientId=clientid
    )
    if 'ClientSecret' in response['UserPoolClient']:
      return response['UserPoolClient']['ClientSecret']
    else:
      return False
  except ClientError as e:
    log_error("response = "+json.dumps(e.response))
    log_error("Error is "+e.response['Error']['Message'])
    return False

def put_ssm_value(session,ssmpath,ssmval):
    client = session.client('ssm')

    try:
      response = client.put_parameter(Name=ssmpath,Value=ssmval,Type='String',Overwrite=True)
      return True
    except ClientError as e:
      log_error("response = "+json.dumps(e.response))
      log_error("Error is "+e.response['Error']['Message'])
      return False

# Begin of main section
parser = OptionParser()
parser.add_option("-a", "--aws", dest="aws",help="AWS Profile")
parser.add_option("-p", "--pool", dest="pool",help="Cognito Client Pool")
parser.add_option("-c", "--client", dest="client",help="Cognito Client Name")
parser.add_option("-s", "--ssmpath", dest="ssmpath",help="SSM path")
parser.add_option("-r", "--region", dest="region",help="AWS Region")

(options, args) = parser.parse_args()

if options.region:
  region = options.region
else:
  region = "us-east-1"

if options.aws:
  session = boto3.Session(profile_name=options.aws,region_name=region)
else:
  session = boto3.Session(region_name=region)

if not options.client:
  Usage()
  exit(1)

if not options.pool:
  Usage()
  exit(1)

if not options.ssmpath:
  Usage()
  exit(1)

secret = get_client_secret(session,options.pool,options.client)
if secret:
  ret = put_ssm_value(session,options.ssmpath,secret)
  if ret:
      print("Added ssm value to path ["+options.ssmpath+"]")
else:
  log_error("Unable to find secret for client ["+options.client+"] within Pool ["+options.pool+"]")
