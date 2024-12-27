from wtforms.fields.choices import SelectField

from app import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product, User, UserRole, ReceiptDetails, Receipt
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
from flask import flash, abort

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())

admin = Admin(app=app, name='E-BOOKSTORE', template_mode='bootstrap4', index_view=MyAdminIndexView())

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class CategoryView(AuthenticatedView):
    can_export = True
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']
    can_view_details = True
    column_list = ['name', 'products']


class ProductView(AuthenticatedView):
    can_export = True
    column_list = ['stt', 'id', 'name', 'category', 'author', 'quantity', 'entry_date']  # Thêm entry_date
    column_labels = {
        'stt': 'STT',
        'id': 'ID',
        'name': 'Tên sách',
        'category': 'Thể loại',
        'author': 'Tác giả',
        'quantity': 'Số lượng',
        'entry_date': 'Ngày nhập'  # Thêm label cho ngày nhập
    }
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'category', 'author', 'entry_date']  # Thêm filter cho ngày nhập
    form_columns = ['name', 'category', 'author', 'quantity', 'entry_date']  # Đảm bảo ngày nhập có thể được nhập

    # Tính STT
    def _stt_formatter(view, context, model, name):
        return view.session.query(view.model).filter(view.model.id <= model.id).count()

    # Ràng buộc kiểm tra khi thêm hoặc sửa dữ liệu
    def on_model_change(self, form, model, is_created):
        if model.quantity < 150:
            flash('⚠️ Số lượng sách phải lớn hơn hoặc bằng 150.', 'warning')
            abort(400)
        if model.quantity > 300:
            flash('⚠️ Không thể nhập, vì số lượng đầu sách trên 300.', 'warning')
            abort(400)

        # Nếu hợp lệ, tiếp tục lưu
        super().on_model_change(form, model, is_created)



class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(MyView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


# class StatsView(MyView):
#     @expose("/")
#     def index(self):
#
#         return self.render('admin/stats.html',
#                            stats=dao.revenue_stats_by_products(),
#                            stats2=dao.revenue_stats_by_time())

class StatsView(MyView):
    @expose("/")
    def index(self):
        # Lấy dữ liệu từ DAO
        revenue_by_category, total_revenue = dao.get_revenue_by_category()
        book_frequency = dao.get_book_frequency()

        # Truyền dữ liệu vào template
        return self.render(
            'admin/stats.html',
            revenue_by_category=revenue_by_category,
            total_revenue=total_revenue,
            book_frequency=book_frequency
        )


class ReceiptView(ModelView):
    """Giao diện hóa đơn - hiển thị chi tiết hóa đơn mở rộng."""

    inline_models = [
        (ReceiptDetails, {
            'form_columns': ['product', 'quantity', 'unit_price', 'total_price'],
        })
    ]

    column_list = ['id', 'user.name', 'created_date', 'details', 'total_amount']
    column_labels = {
        'id': 'Mã hóa đơn',
        'user.name': 'Người lập hóa đơn',
        'created_date': 'Ngày lập hóa đơn',
        'details': 'Chi tiết hóa đơn',
        'total_amount': 'Tổng tiền (VNĐ)'
    }

    column_formatters = {
        'details': lambda view, context, model, name: ', '.join(
            f"{detail.product.name} ({detail.product.category.name}) - {detail.quantity} cuốn"
            for detail in model.details
        )  # Hiển thị tên sách, thể loại và số lượng
    }

    def on_model_change(self, form, model, is_created):
        # Tự động tính tổng tiền hóa đơn
        model.total_amount = sum(detail.quantity * detail.unit_price for detail in model.details)
        super().on_model_change(form, model, is_created)

inline_models = [
    (ReceiptDetails, {
        'form_columns': ['product', 'quantity', 'unit_price', 'total_price'],
        'form_extra_fields': {
            'product': SelectField(
                'Tên sách',
                choices=[(p.id, f"{p.name} ({p.category.name})") for p in Product.query.all()],  # Thêm thể loại
            )
        },
    })
]


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(AuthenticatedView(User, db.session))
admin.add_view(ReceiptView(Receipt, db.session, name='Hóa đơn - bán sách'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
