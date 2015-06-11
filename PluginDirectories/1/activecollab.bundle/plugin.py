import json, urllib2, base64, logging

def results(fields, original_query):
  
  command = fields['command']
  text = fields['~text']

  settings = json.load(open("preferences.json"))
  api_key = settings.get('api_key')
  acInstanceUrl = settings.get('ac_instance_url')
    
  if acInstanceUrl is None or acInstanceUrl=='':
    return {
	    "title": "activeCollab '{0}'".format(command),
	    "run_args": [''],
		"html": "<h2 style='font-family: sans-serif; padding: 2em'>Enter your activeCollab instance URL in the plugin settings</h2>"
	}
    
  if api_key is None or api_key == '':
    return {
	    "title": "activeCollab '{0}'".format(command),
	    "run_args": ['NO_CREDENTIALS', ''],
		"html": "<h2 style='font-family: sans-serif; padding: 2em'>Enter your activeCollab API key in the plugin settings</h2>"
	}
  else:
    results = search_suggest(api_key, text)
    for x in xrange(0,len(results)):
      return {
        "title": "{0}".format(results[x].get('name')),
        "run_args": [ acInstanceUrl + results[x].get('url_path')],
        "html": """
        <script>setTimeout(function() { window.location = %s }, 500);</script>
        """%( acInstanceUrl + results[x].get('url_path') ),
        "webview_user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
        "webview_links_open_in_browser": True
        }
        

def run(url):
  post_notification('Run!')
  import os
  os.system('open "{0}"'.format(url))
  #if command=='project':
#    logging.info('hello!')
#    projects = get_all_projects(api_key)
#    projectId = get_project_id(text, projects)
#    if projectId is None:
# post_notification('Couldn\'t find your project')
#        return
#    post_notification('You selected project {0}'.format(projectId))
#    result = set_chosen_project(text)
#    
#  elif command=='task':
#    post_notification('commanded a task')
#  elif command=='search':
#    results = search_suggest(api_key, text)
#    
#  else:
#    post_notification('no command?')

  #chosenProject = get_chosen_project()
  #if chosenProject is None:
#    post_notification('Please select an existing project in settings: acollab project <project name>')
#    return
#  else:
#    post_notification('Selected project is {0}'.format(chosenProject))

  #projects = get_all_projects(api_key)
  #if projects is None:
  #	post_notification('Please check your activeCollab API key')
  #	return
  #post_notification(projects[0].get('name'))
    
  #chosen_space = get_chosen_project()
  #space_id = get_project_id(chosen_space, projects)
  #if space_id is None:
  #  post_notification('Failed to find your activeCollab project')
  #  return
  #user_id = get_user_id(api_key)
  #create_task(user_id, space_id, task, api_key)
  #post_notification('activeCollab task has been created!')



def search_suggest(api_key, keyword):
  request = urllib2.Request( "https://app.activecollab.com/103607/api/v1/search/suggest?q={0}".format(keyword) )
  #base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')
  request.add_header("X-Angie-AuthApiToken", api_key)   
  try:
    result = urllib2.urlopen(request)
    #projects = json.load(result).get('data')
    results = json.load(result)
  except:
    projects = None
  return results

def format_search_results(results):
  html = "";
  for x in xrange(0,len(results)):
    #html = html + results[x].get('name')
    html = html + "<div><a href='https://app.activecollab.com/103607" + results[x].get('url_path') + "'>" + results[x].get('name') + "</a></div>"
  return html

def get_all_projects(api_key):
  request = urllib2.Request("https://app.activecollab.com/103607/api/v1/projects")
  #base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')
  request.add_header("X-Angie-AuthApiToken", api_key)   
  try:
    result = urllib2.urlopen(request)
    #projects = json.load(result).get('data')
    projects = json.load(result)
  except:
    projects = None
  return projects

    
def get_project_id( projectName, projects):
  project_id = None
  for x in xrange(0,len(projects)):
    if projects[x].get('name') == projectName:
      project_id = projects[x].get('id')
      break
  return project_id


def get_chosen_project():
  settings = json.load(open("preferences.json"))
  project = settings.get('project')
  return project

def set_chosen_project(projectName):
  settings = json.load(open("preferences.json"))
  return settings.set('project', projectName)
  

def create_task(user_id, space_id, task, api_key):
  task_data = {"data" : {"project" : space_id, "name" : task, "assignee": {"id": user_id}}}
  request = urllib2.Request(url="https://app.asana.com/api/1.0/tasks", data=json.dumps(task_data))
  base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)   
  request.add_header('Content-Type', 'application/json')
  result = urllib2.urlopen(request)

def get_user_id(api_key):
  request = urllib2.Request("https://app.asana.com/api/1.0/users/me")
  base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)   
  result = urllib2.urlopen(request)
  user_id = json.load(result).get('data').get('id')
  return user_id



def post_notification(message, title="Flashlight"):
  import os, json, pipes
  # do string escaping:
  message = json.dumps(message)
  title = json.dumps(title)
  script = 'display notification {0} with title {1}'.format(message, title)
  os.system("osascript -e {0}".format(pipes.quote(script)))
