from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from wtforms.fields.numeric import FloatField

from eapp import app, db
from eapp.models import Category, Product, UserRoleEnum
from flask_login import logout_user, current_user
from flask import redirect, render_template

admin = Admin(app=app, name="E-commerce's Admin")

class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class ProductView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_searchable_list = ['name']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    column_filters = ['id', 'name', 'price']
    form_overrides = {
        'price': FloatField
    }

class BaseAuthenticatedView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class StatsView(BaseAuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
        
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin.add_view(AuthenticatedView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='THỐNG KÊ' ))
admin.add_view(LogoutView(name='ĐĂNG XUẤT' ))
