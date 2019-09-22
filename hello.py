from datetime import datetime

from flask import Flask, request, render_template, session, redirect, url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace with secure key'

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


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

