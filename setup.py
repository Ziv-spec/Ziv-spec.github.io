import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST_NAME = "localhost"
PORT = 8080

SITE_NAME = "House Of Useless Thoughts"

EXCLUDE = [ 
  'links.html'
]

def generate_excluded_posts(path):
  POST_TITLE, POST_DATE = '', ''
  content = ''
  with open(path, 'r', encoding='utf-8') as f: 
    lines = f.read().split('\n')

    for line in lines[:4]: 
      if 'title:' in line: 
        POST_TITLE = line[len('title:'):]
      elif 'date:' in line: 
        POST_DATE = line[len('date:'):]
    
    for line in lines[4:]:
      content += line + '\n'

  result = f"""
<head>
<title>{POST_TITLE}</title>
</head>

<h1>{POST_TITLE}</h1>
<i>{POST_DATE}</i>
{content}
"""
  with open('posts/' + path, 'w', encoding='utf-8') as f:
    f.write(result)

def generate_posts(path):
  if not path.endswith('.html') or path == 'index.html':
    return

  if path in EXCLUDE:
    generate_excluded_posts(path)
    return

  POST_TITLE, POST_DATE = '', ''
  content = ''

  with open(path, 'r', encoding='utf-8') as f: 
    lines = f.read().split('\n')

    for line in lines[:4]: 
      if 'title:' in line: 
        POST_TITLE = line[len('title:'):]
      elif 'date:' in line: 
        POST_DATE = line[len('date:'):]

    for line in lines[4:]: 
      l = line[:2] if len(line) > 0 else line
      if l == '' or l == '<h' or l == '<p': l = line + '\n'
      else: l = '<p>' + line + '</p>\n'
      content += l
      
  result = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<title>{POST_TITLE}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:type" content="article" />
<link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
<main class="container flex">
<div class="side"><div class="menu"> 
<h4><a href="/" style="color: #626262; text-decoration: solid;">{SITE_NAME}</a></h4>
<nav id="navigation-bar"></nav>
</div></div>

<div class="wrapper">
<h1 style="line-height: 0.1; ">{POST_TITLE}</h1>
<i>{POST_DATE}</i>
{content}
</div>

<div class="side"> <div class="menu"></div></div>

<script src="side.js"></script>
</body>
</main>
</body>
</html>
  """

  with open('posts/' + path, 'w', encoding='utf-8') as post:
    post.write(result)


def read_html_template(path):
  if 'posts' in path:
    generate_posts(path[len('posts/'):])
  else: 
    generate_posts(path)

  err = False 
  try:
    with open(path, 'r', encoding='utf-8') as f:
      file = f.read()
  except Exception as e:
    file = e
    err = True
  return file, err

class PythonServer(SimpleHTTPRequestHandler):

  def do_GET(self):
    if self.path == '/':
      self.path = '/index.html'

    if self.path is not None:
      content, err = read_html_template(self.path[1:]) 
      if err: 
        self.send_response(404, "File not found")
        content = '<body><h1 style="text-align: center;color: red;">404 ERROR, FILE NOT FOUND<h1></body>'
      else: 
        self.send_response(200, "OK")
      self.end_headers()
      self.wfile.write(bytes(content, "utf-8"))
              
  def do_POST(self):
    pass

if __name__ == "__main__":

  # generate posts
  import os 
  for file in os.listdir():
    if file.endswith('.html') and 'index' not in file and file not in EXCLUDE:
      generate_posts(file)
  for path in EXCLUDE: 
    if path == 'index.html': continue
    generate_excluded_posts(path)

  # create server
  server = HTTPServer((HOST_NAME, PORT), PythonServer)
  print(f"Server started http://{HOST_NAME}:{PORT}")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.server_close()
    print("Server stopped successfully")
    sys.exit(0)
