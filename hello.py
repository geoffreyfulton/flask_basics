from datetime import datetime

from flask import Flask, request, render_template
app = Flask(__name__)

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

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
    return render_template('user.html', name=name)


# Error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




# Programmatically execute app
# if __name__ == '__main__':
#   app.run(debug=True)

