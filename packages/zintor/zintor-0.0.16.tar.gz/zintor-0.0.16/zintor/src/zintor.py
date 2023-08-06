import os.path as op
from uuid import uuid4

from flask import url_for, g, redirect, render_template, request
from flask import has_app_context
from flask_admin import Admin, AdminIndexView, helpers, expose
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

class ZinIndexView(AdminIndexView):
    pass

class Zintor(Admin):
    def __init__(self, app, 
                name='admin', 
                iview=ZinIndexView(), 
                base='admin/base.html',
                ver_ui='bootstrap3',
                ):
        if app.config:
            app.config.update(FLASK_ADMIN_SWATCH='paper')
        Admin.__init__(
            self, 
            app, 
            name=name, 
            index_view=iview,
            base_template=base,
            template_mode=ver_ui,
        )
    
    def set_views(self, views=[]):
        for v in views:
            self.add_view(v)
