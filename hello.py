from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/about')
def about():
    return '<h1>About</h1>'

@app.route('/client-info')
def client_info():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p><p>Your IP Address is {}</p>'.format(user_agent, request.remote_addr)


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
#   app.run(debug=True)

