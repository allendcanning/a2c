import json
import os, time
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Set timezone
os.environ['TZ'] = 'US/Eastern'
time.tzset()

# Open DB connection
dynamodb = boto3.resource('dynamodb')

# This information needs to move to paramater store
table_name = "user_info"
s3_html_bucket = "a2c-html-530317771161"

# Connect to dynamo db table
t = dynamodb.Table(table_name)

def log_error(msg):
  print(msg)

def user_lookup(token):
  return False

def get_user_data(username):
  user_record = {}

  try:
    user_record = t.get_item(
      Key={ 'id': username
          }
      )
  except ClientError as e:
    log_error("Error is "+e.response['Error']['Message'])

  return user_record

def display_info(record):
  user_record = '<div class="divTable">\n'
  user_record += '<div class="divTableBody">\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell"><strong>Personal Information:</strong></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">Name: '
  if 'first' in record:
    user_record += record['first']+' '
  else:
    user_record += '&nbsp; '
  if 'last' in record:
    user_record += record['last']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">Email: '
  if 'email' in record:
    user_record += record['email']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'
   
  user_record += '<div class="divTableCell">Phone: '
  if 'phone' in record:
    user_record += record['phone']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">Address: '
  if 'address' in record:
    user_record += record['address']+', '
  else:
    user_record += '&nbsp;, '
  if 'city' in record:
    user_record += record['city'],' '
  else:
    user_record += '&nbsp; '
  if 'state' in record:
    user_record += record['state'],' '
  else:
    user_record += '&nbsp; '
  if 'zip' in record:
    user_record += record['zip']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow"></div>\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell"><strong>Academic Information:</strong></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'

  user_record += '<div class="divTableCell">GPA: '
  if 'gpa' in record:
    user_record += record['gpa']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">Rank: '
  if 'rank' in record:
    user_record += record['rank']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">YOG: '
  if 'yog' in record:
    user_record += record['yog']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">ACT: '
  if 'act' in record:
    user_record += record['act']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableCell">SAT: '
  if 'satw' in record:
    if 'satm' in record:
      user_record += record['satw'] + record['satm']
      user_record += '(M: '+record['satm']+'; W: '+record['satw']+')'
  else:
    user_record += 'N/A (M: N/A; W: N/A)'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow"></div>\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell"><strong>Athletic Information:</strong></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Sport: '
  if 'sport' in record:
    user_record += record['sport']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  return user_record

def lambda_handler(event, context):
  # Get jwt token
  log_error("Event = "+json.dumps(event))
  if 'headers' in event:
    if 'Authorization' in event['headers']:
      token = event['headers']['Authorization']
    else:
      token = False
  else:
    token = False

  # Verify token and get username
  if token != False:
    username = user_lookup(token)
  else:
    username = False

  css = '<link rel="stylesheet" href="https://s3.amazonaws.com/'+s3_html_bucket+'/css/a2c.css" type="text/css" />'
  content = "<html><head><title>A2C Portal</title>\n"
  content += css+'</head>'
  content += "<body><h3>A2C Portal</h3>"

  # Get user data
  if username != False:
    record = get_user_data(username)
  else:
    record = {}

  # Display user data
  portal_info = display_info(record)

  content += portal_info

  content += "</body></html>"

  return content
