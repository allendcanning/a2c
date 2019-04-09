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
      Key={ 'username': username
          }
      )
  except ClientError as e:
    log_error("Error is "+e.response['Error']['Message'])

  if 'username' not in user_record:
    user_record = {
      'username': username
    }

  return user_record

def display_edit_info(editarea,record):
  edit_record = '<form method="post" action="">'
  if editarea == 'personal':
    edit_record += 'First name: <input type="text" name="first" value="'
    if 'first' in record:
      edit_record += record['first']
    edit_record += '>'
    edit_record += 'Last name: <input type="text" name="last" value="'
    if 'last' in record:
      edit_record += record['last']
    edit_record += '>'
    edit_record += 'Email: <input type="email" name="email" value="'
    if 'email' in record:
      edit_record += record['email']
    edit_record += '>'
    edit_record += 'Phone: <input type="text" name="phone" value="'
    if 'phone' in record:
      edit_record += record['phone']
    edit_record += '>'
    edit_record += 'Address: <input type="text" name="address" value="'
    if 'address' in record:
      edit_record += record['address']
    edit_record += '>'
    edit_record += 'City: <input type="text" name="city" value="'
    if 'city' in record:
      edit_record += record['city']
    edit_record += '>'
    edit_record += 'State: <input type="text" name="state" value="'
    if 'state' in record:
      edit_record += record['state']
    edit_record += '>'
    edit_record += 'Zip: <input type="text" name="zip" value="'
    if 'zip' in record:
      edit_record += record['zip']
    edit_record += '>'
    edit_record += 'Date of Birth: <input type="text" name="dob" value="'
    if 'dob' in record:
      edit_record += record['dob']
    edit_record += '>'
    edit_record += 'Parents: <input type="text" name="parents" value="'
    if 'parents' in record:
      edit_record += record['parents']
    edit_record += '>'
    edit_record += 'Parents Email: <input type="email" name="parentsemail" value="'
    if 'parentsemail' in record:
      edit_record += record['parentsemail']
    edit_record += '>'
    edit_record += 'Parents Phone: <input type="text" name="parentsphone" value="'
    if 'parentsphone' in record:
      edit_record += record['parentsphone']
    edit_record += '>'

  edit_record += '</form>'
  return edit_record

def display_info(record):
  user_record = '<div class="divTable">\n'
  user_record += '<div class="divTableBody">\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Personal Information:</strong> <a href="/?editarea=personal&username='+record['username']+'">Edit</a></div>'
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

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Email: '
  if 'email' in record:
    user_record += record['email']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'
   
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Phone: '
  if 'phone' in record:
    user_record += record['phone']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
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

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Date of Birth: '
  if 'dob' in record:
    user_record += record['dob']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Parents: '
  if 'parents' in record:
    user_record += record['parents']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Parents Email: '
  if 'parentsemail' in record:
    user_record += record['parentsemail']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Parents Phone: '
  if 'parentsphone' in record:
    user_record += record['parentsphone']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow"></div>\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Academic Information:</strong></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">GPA: '
  if 'gpa' in record:
    user_record += record['gpa']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">Rank: '
  if 'rank' in record:
    user_record += record['rank']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">YOG: '
  if 'yog' in record:
    user_record += record['yog']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">ACT: '
  if 'act' in record:
    user_record += record['act']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">SAT: '
  if 'satw' in record:
    if 'satm' in record:
      user_record += record['satw'] + record['satm']
      user_record += '(M: '+record['satm']+'; W: '+record['satw']+')'
  else:
    user_record += 'N/A (M: N/A; W: N/A)'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Athletic Information:</strong></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Sport: '
  if 'sport' in record:
    user_record += record['sport']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">Position: '
  if 'position' in record:
    user_record += record['position']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Strong hand: '
  if 'hand' in record:
    user_record += record['hand']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">Height: '
  if 'height' in record:
    user_record += record['height']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'

  user_record += '<div class="divTableCell">Weight: '
  if 'weight' in record:
    user_record += record['weight']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">Other sports: '
  if 'othersports' in record:
    user_record += record['othersports']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading">Athletic Statistics: '
  if 'stats' in record:
    user_record += record['stats']
  else:
    user_record += '&nbsp;'
  user_record += '</div>'
  user_record += '</div>\n'

  # End of table body and table
  user_record += "</div>\n</div>"
  return user_record

def lambda_handler(event, context):
  token = False
  # Get jwt token
  log_error("Event = "+json.dumps(event))
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
    if 'editarea' in event['queryStringParameters']:
      editarea = event['queryStringParameters']['editarea'] 
    else:
      editarea = False

  css = '<link rel="stylesheet" href="https://s3.amazonaws.com/'+s3_html_bucket+'/css/a2c.css" type="text/css" />'
  content = "<html><head><title>A2C Portal</title>\n"
  content += css+'</head>'
  content += "<body><h3>A2C Portal</h3>"

  # Get user data
  if username != False:
    record = get_user_data(username)
  else:
    record = {}

  # Check for editing
  if editarea != False:
    display_edit_info(editarea,record)

  # Display user data
  portal_info = display_info(record)

  content += portal_info

  content += "</body></html>"

  return { 'statusCode': 200,
           'headers': {
              'Content-type': 'text/html'
           },
           'body': content
         }
