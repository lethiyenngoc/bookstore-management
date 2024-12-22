import math
from flask import render_template, request, redirect, session, jsonify
import dao, utils
from app import app, login
from flask_login import login_user, logout_user, login_required
from app.models import UserRole
from vnpay import create_vnpay_url
import hashlib
import hmac


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1)

    prods = dao.load_products(kw=kw, category_id=cate_id, page=int(page))

    total = dao.count_products()
    return render_template('index.html', products=prods,
                           pages=math.ceil(total/app.config["PAGE_SIZE"]))


@app.route('/products/<int:product_id>')
def details(product_id):
    return render_template('details.html',
                           product=dao.get_product_by_id(product_id),
                           comments=dao.load_comments(product_id))


@app.route('/api/products/<int:product_id>/comments', methods=['post'])
def add_comment(product_id):
    content = request.json.get('content')
    c = dao.add_comment(content=content, product_id=product_id)
    return jsonify({
        'content': c.content,
        'created_date': c.created_date,
        'user': {
            'avatar': c.user.avatar
        }
    })


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route("/login", methods=['get', 'post'])
def login_view():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect(next if next else '/')

    return render_template('login.html')


@app.route('/login-admin', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def register_process():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']

            avatar = request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    # """
    # {
    #     "1": {
    #         "id": "1",
    #         "name": "iPhone",
    #         "price": 30,
    #         "quantity": 2
    #     }, "2": {
    #         "id": "2",
    #         "name": "iPhone",
    #         "price": 30,
    #         "quantity": 1
    #     }
    # }
    # """
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    print(cart)

    return jsonify(utils.stats_cart(cart))


# @app.route('/bookdetails')
# def bookdetails():
    # Fetch book details from the database or another source using book_id
    # book = get_book_by_id(book_id)  # A function to retrieve book data
#     return render_template('bookdetails.html')

#
# @app.route('/bookdetails/<int:book_id>')
# def bookdetails(book_id):
#     # Fetch book details from the database or another source using book_id
#     book = get_book_by_id(book_id)  # A function to retrieve book data
#     return render_template('bookdetails.html', book=book)
#

@app.route("/api/carts/<product_id>", methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = int(request.json.get('quantity', 0))
        cart[product_id]['quantity'] = quantity

        session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route("/api/carts/<product_id>", methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

        session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    cart = session.get('cart')
    try:
        dao.add_receipt(cart)
    except:
        return jsonify({'status': 500})
    else:
        del session['cart']
        return jsonify({'status': 200})

@app.route('/cart')
def cart_view():
    return render_template('cart.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_response_data():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.cart_stats(session.get('cart'))
    }

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_method = request.form.get('payment_method')
    order_id = ""  # Thay bằng ID đơn hàng thực tế
    total_amount = 500000  # Tổng số tiền (VNĐ)
    return_url = "http://localhost:5000/payment_return"

    if payment_method == "vnpay":
        payment_url = create_vnpay_url(order_id, total_amount, return_url)
        return redirect(payment_url)
    elif payment_method == "cash":
        return "Thanh toán tiền mặt, vui lòng chuẩn bị tiền!"
    return "Phương thức thanh toán không hợp lệ!"

@app.route('/payment_return')
def payment_return():
    vnp_response = request.args.to_dict()
    vnp_secure_hash = vnp_response.pop("vnp_SecureHash", None)

    # Kiểm tra chữ ký hợp lệ
    secret_key = "4S5PEP19803HUJBCDHV44JRNNMQ55MQL"  # Thay bằng HashSecret của bạn
    sorted_data = sorted(vnp_response.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_data])

    computed_hash = hmac.new(
        bytes(secret_key, "utf-8"),
        bytes(query_string, "utf-8"),
        hashlib.sha512,
    ).hexdigest()

    if computed_hash == vnp_secure_hash:
        return f"Thanh toán thành công! Mã giao dịch: {vnp_response.get('vnp_TxnRef')}"
    return "Thanh toán thất bại hoặc bị giả mạo!"


if __name__ == '__main__':
    with app.app_context():
        from app import admin
        app.run(debug=True)
