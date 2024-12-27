from app.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return Category.query.order_by('id').all()

# def load_products(kw=None, category_id=None, page=1):
#     products = Product.query
#
#     if kw:
#         products = products.filter(Product.name.contains(kw))
#
#     if category_id:
#         products = products.filter(Product.category_id == category_id)
#
#     page_size = app.config["PAGE_SIZE"]
#     start = (page - 1) * page_size
#     products = products.slice(start, start + page_size)
#
#     return products.all()

def load_products(kw=None, category_id=None, page=1, sort_order='asc'):
    products = Product.query
    # keyword filter
    if kw:
        products = products.filter(Product.name.contains(kw))
    # category filter
    if category_id:
        products = products.filter(Product.category_id == category_id)
    # sort
    if sort_order == 'asc':
        products = products.order_by(Product.price.asc())
    else:
        products = products.order_by(Product.price.desc())
    #
    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    products = products.offset(start).limit(page_size)

    return products.all()


def load_products2(kw=None, category_id=None, page=1):
    query = Product.query.order_by(Product.id)

    # Tìm theo từ khóa
    if kw and isinstance(kw, str):
        query = query.filter(Product.name.contains(kw))

    # Tìm theo danh mục
    if category_id and isinstance(category_id, int):
        query = query.filter(Product.category_id == category_id)

    # Số lượng sản phẩm trên mỗi trang
    page_size = app.config.get('PAGE_SIZE', 6)

    # Paginate
    return query.paginate(page=page, per_page=page_size, error_out=False)

def count_products2(category_id=None):
    query = Product.query

    # Đếm sản phẩm theo thể loại
    if category_id and isinstance(category_id, int):
        query = query.filter(Product.category_id == category_id)

    return query.count()

def get_category_by_id(category_id):
    category = Category.query.get(category_id)
    if not category:
        raise ValueError(f"Category with ID {category_id} not found.")
    return category

def get_all_categories():
    return Category.query.order_by(Category.name).all()



def count_products():
    return Product.query.count()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg')

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)

def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               product_id=c['id'], receipt=r)
            db.session.add(d)
        db.session.commit()


def revenue_stats_by_products():
    return db.session.query(Product.id, Product.name,
                            func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price))\
             .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))\
             .group_by(Product.id).all()

# def revenue_stats_by_time(time='month', year=datetime.now().year):
#     return db.session.query(func.extract(time, Receipt.created_date),
#                             func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)) \
#         .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
#         .group_by(func.extract(time, Receipt.created_date))\
#         .filter(func.extract('year', Receipt.created_date).__eq__(year))\
#         .order_by(func.extract(time, Receipt.created_date)).all()

def get_revenue_by_category():
    data = db.session.query(
        Category.name.label('category'),
        func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label('revenue'),
        func.count(ReceiptDetails.id).label('rent_count')
    ).join(Product, Product.category_id == Category.id) \
        .join(ReceiptDetails, ReceiptDetails.product_id == Product.id) \
        .group_by(Category.name).all()

    total_revenue = sum(row.revenue for row in data)

    result = []
    for row in data:
        result.append({
            'category': row.category,
            'revenue': row.revenue,
            'rent_count': row.rent_count,
            'percentage': round(row.revenue / total_revenue * 100, 2) if total_revenue > 0 else 0
        })

    return result, total_revenue


def get_book_frequency():
    data = db.session.query(
        Product.name.label('book_name'),
        Category.name.label('category'),
        func.sum(ReceiptDetails.quantity).label('quantity')
    ).join(Product, Product.id == ReceiptDetails.product_id) \
        .join(Category, Category.id == Product.category_id) \
        .group_by(Product.name, Category.name).all()

    total_quantity = sum(row.quantity for row in data)

    result = []
    for row in data:
        result.append({
            'book_name': row.book_name,
            'category': row.category,
            'quantity': row.quantity,
            'percentage': round(row.quantity / total_quantity * 100, 2) if total_quantity > 0 else 0
        })

    return result


def get_invoice_by_customer(customer_id):
    # Lấy thông tin hóa đơn từ database dựa trên ID khách hàng
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    invoices = db.session.query(Invoice).filter_by(customer_id=customer_id).all()

    return {
        "customer_name": customer.name,
        "created_date": invoices[0].created_date if invoices else None,
        "items": [
            {
                "book_name": item.product.name,
                "category": item.product.category.name,
                "quantity": item.quantity,
                "price": item.product.price
            }
            for item in invoices
        ]
    }



def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id).all()


def get_product_by_id(id):
    return Product.query.get(id)

def load_comments(product_id):
    comments = Comment.query.filter(Comment.product_id == product_id).order_by(-Comment.id).all()
    print([c.content for c in comments])
    return comments


def add_comment(content, product_id, user_id, rating):
    if not content:
        raise ValueError("Content cannot be empty")

    c = Comment(content=content, product_id=product_id, user_id=user_id, rating=rating)
    db.session.add(c)
    db.session.commit()
    return c


if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())