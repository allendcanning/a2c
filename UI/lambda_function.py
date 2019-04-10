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

def update_user_info(record):
  # Add some error handling
  t.put_item(Item=record)

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
    user_record['usename'] = username

  return user_record

def edit_personal_info(record):
  user_record = '<form method="post" action="">\n'
  user_record += '<input type="hidden" name="action" value="Process">\n'
  user_record += '<input type="hidden" name="username" value="'+record['username']+''">\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Personal Information:</strong> <input type="submit" name="Submit"></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'First name: <input type="text" name="first" value="'
  if 'first' in record:
    user_record += record['first']
  user_record += '">'
  user_record += '</div>'
  user_record += '<div class="divTableCell">'
  user_record += 'Last name: <input type="text" name="last" value="'
  if 'last' in record:
    user_record += record['last']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Email: <input type="email" name="email" value="'
  if 'email' in record:
    user_record += record['email']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Phone: <input type="text" name="phone" value="'
  if 'phone' in record:
    user_record += record['phone']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Address: <input type="text" name="address" value="'
  if 'address' in record:
    user_record += record['address']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'City: <input type="text" name="city" value="'
  if 'city' in record:
    user_record += record['city']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'State: <input type="text" name="state" value="'
  if 'state' in record:
    user_record += record['state']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Zip: <input type="text" name="zip" value="'
  if 'zip' in record:
    user_record += record['zip']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Date of Birth: <input type="text" name="dob" value="'
  if 'dob' in record:
    user_record += record['dob']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Parents: <input type="text" name="parents" value="'
  if 'parents' in record:
    user_record += record['parents']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Parents Email: <input type="email" name="parentsemail" value="'
  if 'parentsemail' in record:
    user_record += record['parentsemail']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Parents Phone: <input type="text" name="parentsphone" value="'
  if 'parentsphone' in record:
    user_record += record['parentsphone']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '</form>'
  return user_record

def edit_academic_info(record):
  user_record = '<form method="post" action="">'
  user_record += '<input type="hidden" name="action" value="Process">\n'
  user_record += '<input type="hidden" name="username" value="'+record['username']+''">\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Academic Information:</strong> <input type="submit" name="Submit"></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'GPA: <input type="text" name="gpa" value="'
  if 'gpa' in record:
    user_record += record['gpa']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Rank: <input type="text" name="rank" value="'
  if 'rank' in record:
    user_record += record['rank']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Year of Graduation: <select name="yog">'
  for y in range(2020,2028):
    user_record += '<option value="'+str(y)+'"'
    if 'yog' in record:
      if record['yog'] == y:
        user_record += ' selected'
    user_record += '>'+str(y)+'</option>'
  user_record += '</select>'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'ACT: <input type="text" name="act" value="'
  if 'act' in record:
    user_record += record['act']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'SAT Math: <input type="text" name="satm" value="'
  if 'satm' in record:
    user_record += record['satm']
  user_record += '">'
  user_record += '</div>'
  user_record += '<div class="divTableCell">'
  user_record += 'SAT Writing: <input type="text" name="satw" value="'
  if 'satw' in record:
    user_record += record['satw']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  return user_record

def edit_athletic_info(record):
  user_record = '<form method="post" action="">'
  user_record += '<input type="hidden" name="action" value="Process">\n'
  user_record += '<input type="hidden" name="username" value="'+record['username']+''">\n'
  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Athletic Information:</strong> <input type="submit" name="Submit"></div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Sport: <input type="text" name="sport" value="'
  if 'sport' in record:
    user_record += record['sport']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Position: <input type="text" name="position" value="'
  if 'position' in record:
    user_record += record['position']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Strong hand: <select name="stronghand">'
  hands = ['Right', 'Left']
  for h in hands:
    user_record += '<option value="'+h+'"'
    if 'stronghand' in record:
      if record['stronghand'] == h:
        user_record += ' selected'
    user_record += '>'+h+'</option>'
  user_record += '</select>'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Height: <input type="text" name="height" value="'
  if 'height' in record:
    user_record += record['height']
  user_record += '">'
  user_record += '</div>'

  user_record += '<div class="divTableCell">'
  user_record += 'Weight: <input type="text" name="weight" value="'
  if 'weight' in record:
    user_record += record['weight']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  user_record += '<div class="divTableRow">\n'
  user_record += '<div class="divTableCell">'
  user_record += 'Other Sports: <input type="text" name="othersports" value="'
  if 'othersports' in record:
    user_record += record['othersports']
  user_record += '">'
  user_record += '</div>'
  user_record += '</div>\n'

  return user_record

def display_personal_info(record):
  user_record = '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Personal Information:</strong> <a href="/Stage/?editarea=personal&username='+record['username']+'">Edit</a></div>'
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
  
  return user_record

def display_academic_info(record):
  user_record = '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Academic Information:</strong> <a href="/Stage/?editarea=academic&username='+record['username']+'">Edit</a></div>'
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

  return user_record

def display_athletic_info(record):
  user_record = '<div class="divTableRow">\n'
  user_record += '<div class="divTableHeading"><strong>Athletic Information:</strong> <a href="/Stage/?editarea=athletic&username='+record['username']+'">Edit</a></div>'
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

  return user_record

def lambda_handler(event, context):
  token = False
  user_record = {}
  user_record['action'] = "Form"

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
    if 'editarea' in event['queryStringParameters']:
      editarea = event['queryStringParameters']['editarea'] 
    else:
      editarea = False

  if 'body' in event:
    if event['body'] != None:
      # Parse the post parameters
      postparams = event['body']
      user_record = {}
      user_record['username'] = username
      for token in postparams.split('&'):
        key = token.split('=')[0]
        if key == "Submit":
          continue
        value = token.split('=')[1]
        user_record[key] = unquote_plus(value)

  # If we have form data, update dynamo
  if 'action' in user_record:
    if user_record['action'] == "Process":
      del user_record['action']
      update_user_info(user_record)
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

  content += '<div class="divTable">\n'
  content += '<div class="divTableBody">\n'

  # Check for editing
  if editarea == "personal":
    content += edit_personal_info(record)
    content += display_academic_info(record)
    content += display_athletic_info(record)
  elif editarea == "academic":
    content += display_personal_info(record)
    content += edit_academic_info(record)
    content += display_athletic_info(record)
  elif editarea == "athletic":
    content += display_personal_info(record)
    content += display_academic_info(record)
    content += edit_athletic_info(record)
  else:
    content += display_personal_info(record)
    content += display_academic_info(record)
    content += display_athletic_info(record)

  # End of table body and table
  content += "</div>\n</div>"

  content += "</body></html>"

  return { 'statusCode': 200,
           'headers': {
              'Content-type': 'text/html'
           },
           'body': content
         }
