import os.path as op
from uuid import uuid4

from flask import url_for, g, redirect, render_template, request
from flask import has_app_context
from flask_admin import Admin, helpers, expose
from flask_admin.model.form import InlineFormAdmin
from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from flask_admin.contrib.sqla.filters import FilterEqual, BooleanEqualFilter
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin.contrib.sqla import (
    ModelView,
)
from flask_admin import form
from flask_admin.form import rules
from markupsafe import Markup
from wtforms import fields, widgets, validators
import flask_login as login

def welcome():
    print('Hello, welcome to Z-Admin package.')


def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    parts = (uuid4(), parts[-1])
    return secure_filename('%s%s' % parts)

class BaseView(ModelView):
    column_list = ('id', 'created_at', 'updated_at')
    column_labels = dict(
        id='#',
        created_at='登録日時',
        updated_at='更新日時',
    )
    def is_accessible(self):
        return login.current_user.is_authenticated

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username


class BaseInlineView(InlineFormAdmin):
    pass

class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField(
            '画像',
            base_path='static',
            allowed_extensions=('jpeg', 'jpg', 'png'),
            thumbnail_size=(100, 100, True),
            max_size=(2048, 2048, True),
            namegen=prefix_name,
        )
    }
    
class ImageInlineModelForm(InlineFormAdmin):
    form_columns = ('id', 'path')
    form_extra_fields = {
        'path': form.ImageUploadField(
            '画像',
            base_path='static',
            allowed_extensions=('jpeg', 'jpg', 'png'),
            thumbnail_size=(100, 100, True),
            max_size=(2048, 2048, True),
            namegen=prefix_name,
        )
    }

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(AdminUser).filter_by(login=self.login.data).first()

# customized index view class that handles login & registration
class ZinAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(ZinAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        
        self._template_args['form'] = form
        return super(ZinAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

    # user = User()
    # user.password = generate_password_hash(form.password.data)
    # db.session.add(user)
    # db.session.commit()

# Initialize flask-login
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(AdminUser).get(user_id)

class Zintor(Admin):
    def __init__(self, app, name='admin', base_template='admin/t3base.html'):
        if app.config:
            app.config.update(FLASK_ADMIN_SWATCH='paper')
        Admin.__init__(
            self, 
            app, 
            name=name, 
            index_view=ZinAdminIndexView(),
            base_template=base_template,
            template_mode='bootstrap3',
        )
    
    def set_views(self, views=[]):
        for v in views:
            self.add_view(v)
