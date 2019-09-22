from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


# manually add route
def manual_route():
    return '<h1>This is a manually registered route</h1>'

app.add_url_rule('/manualroute', 'manual_route', manual_route)


# variable routes
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


# Programmatically execute app
# if __name__ == '__main__':
#   app.run()

