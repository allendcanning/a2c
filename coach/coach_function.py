import json
import os, time
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus

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

def get_student_data(username):
  user_record = {}

  log_error("Checking for user "+username)
  try:
    item = t.get_item(
      Key={ 'username': username
          }
      )
    user_record = item['Item']
    log_error("Item = "+json.dumps(user_record))
  except ClientError as e:
    log_error("response = "+json.dumps(e.response))
    log_error("Error is "+e.response['Error']['Message'])

  if 'username' not in user_record:
    user_record['username'] = username

  return user_record

def display_student_info(record):
  user_record = '<tr><td>\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Personal Information:</th></tr>\n'

  user_record += '    <tr><td class="header">Name: </td><td class="data">'
  if 'firstname' in record:
    user_record += record['firstname']+' '
  else:
    user_record += '&nbsp; '
  if 'lastname' in record:
    user_record += record['lastname']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Email: </td><td class="data">'
  if 'email' in record:
    user_record += record['email']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'
   
  user_record += '    <tr><td class="header">Phone: </td><td class="data">'
  if 'phone' in record:
    user_record += record['phone']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Address: </td><td class="data">'
  if 'address' in record:
    user_record += record['address']+', '
  else:
    user_record += '&nbsp;, '
  if 'city' in record:
    user_record += record['city']+' '
  else:
    user_record += '&nbsp; '
  if 'st' in record:
    user_record += record['st']+' '
  else:
    user_record += '&nbsp; '
  if 'zip' in record:
    user_record += record['zip']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Date of Birth: </td><td class="data">'
  if 'dob' in record:
    user_record += record['dob']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents: </td><td class="data">'
  if 'parents' in record:
    user_record += record['parents']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents Email: </td><td class="data">'
  if 'parentsemail' in record:
    user_record += record['parentsemail']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents Phone: </td><td class="data">'
  if 'parentsphone' in record:
    user_record += record['parentsphone']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td>\n'
  
  user_record += '<td class="right">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Academic Information:</th></tr>\n'

  user_record += '    <tr><td class="header">GPA: </td><td class="data">'
  if 'gpa' in record:
    user_record += record['gpa']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Rank: </td><td class="data">'
  if 'classrank' in record:
    user_record += record['classrank']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">YOG: </td><td class="data">'
  if 'yog' in record:
    user_record += record['yog']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">ACT: </td><td class="data">'
  if 'act' in record:
    user_record += record['act']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">SAT: </td><td class="data">'
  if 'satw' in record:
    if 'satm' in record:
      user_record += str(int(record['satw'])+int(record['satm']))
      user_record += ' (M: '+record['satm']+'; W: '+record['satw']+')'
  else:
    user_record += 'N/A (M: N/A; W: N/A)'
  user_record += '    </td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  user_record += '<tr><td colspan="2">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Athletic Information:</th></tr>\n'

  user_record += '    <tr><td class="header">Sport: </td><td class="data">'
  if 'sport' in record:
    user_record += record['sport']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Position: </td><td class="data">'
  if 'position' in record:
    user_record += record['position']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Strong hand: </td><td class="data">'
  if 'stronghand' in record:
    user_record += record['stronghand']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Height: </td><td class="data">'
  if 'height' in record:
    user_record += record['height']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Weight: </td><td class="data">'
  if 'weight' in record:
    user_record += record['weight']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Other sports: </td><td class="data">'
  if 'othersports' in record:
    user_record += record['othersports']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Athletic Statistics: </td><td class="data">'
  if 'stats' in record:
    user_record += record['stats']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  return user_record

def lambda_handler(event, context):
  token = False
  user_record = {}
  user_record['action'] = "Form"

  # Log the event object
  log_error("Event = "+json.dumps(event))

  # Get jwt token
  if 'headers' in event:
    if event['headers'] != None:
      if 'Authorization' in event['headers']:
        token = event['headers']['Authorization']

  # Verify token and get username
  if token != False:
    username = user_lookup(token)
  else:
    username = False

  # Get username from query string, for now
  if 'queryStringParameters' in event:
    if 'username' in event['queryStringParameters']:
      username = event['queryStringParameters']['username']
    elif 'student' in event['queryStringParameters']:
      student = event['queryStringParameters']['student']

  student_record = get_student_data(student)

  css = '<link rel="stylesheet" href="https://s3.amazonaws.com/'+s3_html_bucket+'/css/a2c.css" type="text/css" />'
  content = "<html><head><title>A2C Portal</title>\n"
  content += css+'</head>'
  content += "<body><h3>A2C Portal</h3>"

  content += '<table class="topTable">\n'

  content += display_student_info(student_record)

  # End of table body and table
  content += "</table>\n"

  content += "</body></html>"

  return { 'statusCode': 200,
           'headers': {
              'Content-type': 'text/html'
           },
           'body': content
         }