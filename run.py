import os

from flask import Flask
from jinja2 import Template

app = Flask(__name__)

t = Template("Hello World!")


@app.route('/')
def hello_world():
    return t.render()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', '8234'))
