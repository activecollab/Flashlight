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
    results = search_suggest(api_key, acInstanceUrl, text)
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


def search_suggest(api_key, acInstanceUrl, keyword):
  request = urllib2.Request( acInstanceUrl + "/search/suggest?q={0}".format(keyword) )
  #base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')
  request.add_header("X-Angie-AuthApiToken", api_key)   
  results = ''
  try:
    result = urllib2.urlopen(request)
    #projects = json.load(result).get('data')
    results = json.load(result)
  except:
    results = None
  return results

