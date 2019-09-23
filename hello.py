import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, request, render_template, session, redirect, url_for, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace with secure key'

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# Shell Context Processor for db objects
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())


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

