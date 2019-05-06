import json
import os, time
import re
import boto3
import hmac
import hashlib
import base64
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

# Connect to dynamo db table
t = dynamodb.Table(table_name)

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

def update_user_info(record):
  # Add some error handling
  try:
    for item in record:
      if record[item] == "":
        record[item] = None
    t.put_item(Item=record)
  except ClientError as e:
    log_error("response = "+json.dumps(e.response))
    log_error("Error is "+e.response['Error']['Message'])
  
  return False

def get_user_data(username):
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

def edit_athlete_info(environment,record):
  user_record = '<form method="post" id="Cancel" action="">\n'
  user_record += '</form>'
  user_record += '<form method="post" action="">\n'
  user_record += '<input type="hidden" name="action" value="Process">\n'
  user_record += '<tr><td>\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th colspan="2" class="areaHead">Personal Information:</th><th colspan="6" class="areaHead"><input type="submit" name="Submit"><input class="button" type="button" onclick="document.getElementById(\'Cancel\').submit()" value="Cancel" /></th></tr>'

  user_record += '    <tr><td class="header">First name: </td><td class="data">'

  user_record += '<input type="text" name="firstname" value="'
  if 'firstname' in record:
    if record['firstname'] != None:
      user_record += record['firstname']
  user_record += '">'
  user_record += '</td>'
  user_record += '<td class="header">'
  user_record += 'Last name: </td><td class="data"><input type="text" name="lastname" value="'
  if 'lastname' in record:
    if record['lastname'] != None:
      user_record += record['lastname']
  user_record += '">'
  user_record += '</td>'
  user_record += '</tr>\n'

  user_record += '    <tr><td class="header">Email: <td class="data"><input type="email" name="email" value="'
  if 'email' in record:
    if record['email'] != None:
      user_record += record['email']
  user_record += '">'
  user_record += '</td>'
  user_record += '</tr>\n'

  user_record += '    <tr><td class="header">Phone: <td class="data"><input type="text" name="phone" value="'
  if 'phone' in record:
    if record['phone'] != None:
      user_record += record['phone']
  user_record += '">'
  user_record += '</td>'
  user_record += '</tr>\n'

  user_record += '    <tr><td class="header">Address: <td class="data"><input type="text" name="address" value="'
  if 'address' in record:
    if record['address'] != None:
      user_record += record['address']
  user_record += '">'
  user_record += '</td>'

  user_record += '      <td class="header">City: <td class="data"><input type="text" name="city" value="'
  if 'city' in record:
    if record['city'] != None:
      user_record += record['city']
  user_record += '">'
  user_record += '</td>'

  user_record += '      <td class="header">State: <td class="data"><input type="text" name="st" value="'
  if 'st' in record:
    if record['st'] != None:
      user_record += record['st']
  user_record += '">'
  user_record += '</td>'

  user_record += '      <td class="header">Zip: <td class="data"><input type="text" name="zip" value="'
  if 'zip' in record:
    if record['zip'] != None:
      user_record += record['zip']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Date of Birth: <td class="data"><input type="text" name="dob" value="'
  if 'dob' in record:
    if record['dob'] != None:
      user_record += record['dob']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Parents: <td class="data"><input type="text" name="parents" value="'
  if 'parents' in record:
    if record['parents'] != None:
      user_record += record['parents']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Parents email: <td class="data"><input type="email" name="parentsemail" value="'
  if 'parentsemail' in record:
    if record['parentsemail'] != None:
      user_record += record['parentsemail']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Parents phone: <td class="data"><input type="text" name="parentsphone" value="'
  if 'parentsphone' in record:
    if record['parentsphone'] != None:
      user_record += record['parentsphone']
  user_record += '">'
  user_record += '</td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  # Edit academic info
  user_record += '<td class="right">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th colspan="2" class="areaHead">Academic Information:</th><th colspan="2" class="areaHead"><input type="submit" name="Submit"><input class="button" type="button" onclick="document.getElementById(\'Cancel\').submit()" value="Cancel" /></th></tr>'

  user_record += '    <tr><td class="header">GPA: <td class="data"><input type="text" name="gpa" value="'
  if 'gpa' in record:
    if record['gpa'] != None:
      user_record += record['gpa']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Class Rank: <td class="data"><input type="text" name="classrank" value="'
  if 'classrank' in record:
    if record['classrank'] != None:
      user_record += record['classrank']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Year of Graduation: <td class="data">'
  user_record += '<select name="yog">'
  for y in range(2020,2028):
    user_record += '<option value="'+str(y)+'"'
    if 'yog' in record:
      if record['yog'] == y:
        user_record += ' selected'
    user_record += '>'+str(y)+'</option>'
  user_record += '</select>'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">ACT: <td class="data"><input type="text" name="act" value="'
  if 'act' in record:
    if record['act'] != None
      user_record += record['act']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">SAT Math: <td class="data"><input type="text" name="satm" value="'
  if 'satm' in record:
    if record['satm'] != None:
      user_record += record['satm']
  user_record += '">'
  user_record += '</td>'

  user_record += '<td class="header">SAT Writing: <td class="data"><input type="text" name="satw" value="'
  if 'satw' in record:
    if record['satw'] != None:
      user_record += record['satw']
  user_record += '">'
  user_record += '</td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  # Edit athletic information
  user_record += '<tr><td colspan="2">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Athletic Information:</th><th class="areaHead"><input type="submit" name="Submit"><input class="button" type="button" onclick="document.getElementById(\'Cancel\').submit()" value="Cancel" /></th></tr>'

  user_record += '    <tr><td class="header">Sport: <td class="athletedata"><input type="text" name="sport" value="'
  if 'sport' in record:
    if record['sport'] != None:
      user_record += record['sport']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Position: <td class="athletedata"><input type="text" name="pos" value="'
  if 'pos' in record:
    if record['pos'] != None:
      user_record += record['pos']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Strong hand: <td class="athletedata"><select name="stronghand">'
  hands = ['Right', 'Left']
  for h in hands:
    user_record += '<option value="'+h+'"'
    if 'stronghand' in record:
      if record['stronghand'] == h:
        user_record += ' selected'
    user_record += '>'+h+'</option>'
  user_record += '</select>'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Height: <td class="athletedata"><input type="text" name="height" value="'
  if 'height' in record:
    if record['height'] != None:
      user_record += record['height']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Weight: <td class="athletedata"><input type="text" name="weight" value="'
  if 'weight' in record:
    if record['weight'] != None:
      user_record += record['weight']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Other Sports: <td class="athletedata"><input type="text" name="othersports" value="'
  if 'othersports' in record:
    if record['othersports'] != None:
      user_record += record['othersports']
  user_record += '">'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Athletic Statistics: <td class="athletedata"><textarea rows="10" cols="50" name="athleticstats">'
  if 'athleticstats' in record:
    if record['athleticstats'] != None:
      user_record += record['athleticstats'].replace('<br>', '\n')
  user_record += '</textarea>'
  user_record += '</td></tr>\n'

  user_record += '    <tr><td class="header">Highlight Links: <td class="athletedata"><textarea rows="5" cols="50" name="highlights">'
  if 'highlights' in record:
    if record['highlights'] != None:
      user_record += record['highlights'].replace('<br>', '\n')
  user_record += '</textarea>'
  user_record += '</td></tr>\n'
  
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  user_record += '</form>'

  return user_record

def display_athlete_info(environment,record):
  user_record = '<tr><td>\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Personal Information:</th><th class="areaHead">'
  user_record += '<form method="post" action="">'
  user_record += '<input type="hidden" name="action" value="edit">'
  user_record += '<input type="submit" value="Edit">'
  user_record += '</form></th></tr>\n'

  user_record += '    <tr><td class="header">Name: </td><td class="data">'
  if 'firstname' in record:
    user_record += str(record['firstname'])+' '
  else:
    user_record += '&nbsp; '
  if 'lastname' in record:
    user_record += str(record['lastname'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Email: </td><td class="data">'
  if 'email' in record:
    user_record += str(record['email'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'
   
  user_record += '    <tr><td class="header">Phone: </td><td class="data">'
  if 'phone' in record:
    user_record += str(record['phone'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Address: </td><td class="data">'
  if 'address' in record:
    user_record += str(record['address'])+', '
  else:
    user_record += '&nbsp;, '
  if 'city' in record:
    user_record += str(record['city'])+' '
  else:
    user_record += '&nbsp; '
  if 'st' in record:
    user_record += str(record['st'])+' '
  else:
    user_record += '&nbsp; '
  if 'zip' in record:
    user_record += str(record['zip'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Date of Birth: </td><td class="data">'
  if 'dob' in record:
    user_record += str(record['dob'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents: </td><td class="data">'
  if 'parents' in record:
    user_record += str(record['parents'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents Email: </td><td class="data">'
  if 'parentsemail' in record:
    user_record += str(record['parentsemail'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Parents Phone: </td><td class="data">'
  if 'parentsphone' in record:
    user_record += str(record['parentsphone'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td>\n'
  
  # Display academic information
  user_record += '<td class="right">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Academic Information:</th><th class="areaHead">'
  user_record += '<form method="post" action="">'
  user_record += '<input type="hidden" name="action" value="edit">'
  user_record += '<input type="submit" value="Edit">'
  user_record += '</form></th></tr>\n'

  user_record += '    <tr><td class="header">GPA: </td><td class="data">'
  if 'gpa' in record:
    user_record += str(record['gpa'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Rank: </td><td class="data">'
  if 'classrank' in record:
    user_record += str(record['classrank'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">YOG: </td><td class="data">'
  if 'yog' in record:
    user_record += str(record['yog'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">ACT: </td><td class="data">'
  if 'act' in record:
    if record['act'] != None:
      user_record += record['act']
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">SAT: </td><td class="data">'
  if 'satw' in record:
    if 'satm' in record:
      user_record += str(int(record['satw'])+int(record['satm']))
      user_record += ' (M: '+str(record['satm'])+'; W: '+str(record['satw'])+')'
  else:
    user_record += 'N/A (M: N/A; W: N/A)'
  user_record += '    </td></tr>\n'
  user_record += '  </table>\n'
  user_record += '</td></tr>\n'

  # Display athletic information
  user_record += '<tr><td colspan="2">\n'
  user_record += '  <table class="defTable">\n'
  user_record += '    <tr><th class="areaHead">Athletic Information:</th><th class="areaHead">'
  user_record += '<form method="post" action="">'
  user_record += '<input type="hidden" name="action" value="edit">'
  user_record += '<input type="submit" value="Edit">'
  user_record += '</form></th></tr>\n'

  user_record += '    <tr><td class="header">Sport: </td><td class="data">'
  if 'sport' in record:
    user_record += str(record['sport'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Position: </td><td class="data">'
  if 'pos' in record:
    user_record += str(record['pos'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Strong hand: </td><td class="data">'
  if 'stronghand' in record:
    user_record += str(record['stronghand'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Height: </td><td class="data">'
  if 'height' in record:
    user_record += str(record['height'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Weight: </td><td class="data">'
  if 'weight' in record:
    user_record += str(record['weight'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Other sports: </td><td class="data">'
  if 'othersports' in record:
    user_record += str(record['othersports'])
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Athletic Statistics: </td><td class="data">'
  if 'athleticstats' in record:
    user_record += str(record['athleticstats']).replace('\n', '<br>')
  else:
    user_record += '&nbsp;'
  user_record += '    </td></tr>\n'

  user_record += '    <tr><td class="header">Highlight Links: </td><td class="data">'
  if 'highlights' in record:
    highlights = str(record['highlights'])
    highlights = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', highlights)
    for h in highlights:
      user_record += '<a href="'+h+'">'+h+'</a><br>'
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

  log_error("Event = "+json.dumps(event))

  # Get the environment from the context stage
  environment = event['requestContext']['stage']
  # look up the config data using environment
  #config = get_config_data(environment)
  
  username = event['requestContext']['authorizer']['claims']['cognito:username']
  user_record['username'] = username

  if 'body' in event:
    if event['body'] != None:
      # Parse the post parameters
      postparams = event['body']
      for token in postparams.split('&'):
        key = token.split('=')[0]
        if key == "Submit":
          continue
        value = token.split('=')[1]
        user_record[key] = unquote_plus(value)

  # If we have form data, update dynamo
  if 'action' in user_record:
    action = user_record['action']
    if user_record['action'] == "Process":
      del user_record['action']
      update_user_info(user_record)

  # Get user data
  if username != False:
    record = get_user_data(username)
  else:
    record = {}

  log_error("Record = "+json.dumps(record))
  content = '<table class="topTable">\n'

  # Check for editing
  if action == "edit":
    content += edit_athlete_info(environment,record)
  else:
    content += display_athlete_info(environment,record)

  # End of table body and table
  content += "</table>\n"

  return { 'statusCode': 200,
           'headers': {
              'Content-type': 'text/html',
           },
           'body': content
         }