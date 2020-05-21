from flask import Flask

app = Flask('website', static_folder='views/static', template_folder='views/templates')
