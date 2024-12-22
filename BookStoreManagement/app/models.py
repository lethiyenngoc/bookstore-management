import random
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    productcode = Column(String(20), nullable=True, unique=True)
    author = Column(String(50), nullable=True)
    publisher = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    numberpage = Column(Integer, nullable=True)
    form = Column(String(20), nullable=True)
    size = Column(String(20), nullable=True)
    image = Column(String(255), nullable=True)
    price = Column(Float, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        # u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        #
        # c1 = Category(name='Thiếu nhi')
        # c2 = Category(name='Tâm lý - Kỹ năng sống')
        # c3 = Category(name='Kinh tế')
        # c4 = Category(name='Văn học')
        # c5 = Category(name='Sách ngoại ngữ')
        # c6 = Category(name='Thể loại khác')
        # db.session.add_all([c1, c2, c3, c4, c5, c6])
        # db.session.commit()

        c1 = Comment(content='good', user_id=1, product_id=1)
        c2 = Comment(content='excellent', user_id=1, product_id=1)
        c3 = Comment(content='nice', user_id=1, product_id=1)

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # data = [
        #     # Thiếu nhi
        #     {
        #         "name": "Chú sâu háu ăn",
        #         "productcode": "TN001",
        #         "author": "Eric Carle",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Một câu chuyện thú vị về chú sâu nhỏ ăn rất nhiều.",
        #         "numberpage": 32,
        #         "form": "Bìa mềm",
        #         "size": "20x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734836607/98f6110a-289f-4f94-833b-f2119a195a5d.png",
        #         "price": 50000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Tấm Cám",
        #         "productcode": "TN002",
        #         "author": "Truyện cổ tích Việt Nam",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện cổ tích nổi tiếng của Việt Nam.",
        #         "numberpage": 40,
        #         "form": "Bìa cứng",
        #         "size": "22x22 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734836687/2212e62a-0c52-4de0-ad4a-d53b330c4cf4.png",
        #         "price": 60000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Cô bé quàng khăn đỏ",
        #         "productcode": "TN003",
        #         "author": "Truyện cổ tích Grimm",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện về cô bé quàng khăn đỏ và con sói.",
        #         "numberpage": 36,
        #         "form": "Bìa mềm",
        #         "size": "20x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734836724/efcba5a7-7099-445a-a181-45cbb3e363dd.png",
        #         "price": 55000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Công chúa ngủ trong rừng",
        #         "productcode": "TN004",
        #         "author": "Truyện cổ tích Grimm",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện cổ tích kinh điển về công chúa và lời nguyền.",
        #         "numberpage": 48,
        #         "form": "Bìa cứng",
        #         "size": "22x22 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734836806/042b002d-e604-40bb-8b8b-8485b86b01bb.png",
        #         "price": 65000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Ba chú lợn con",
        #         "productcode": "TN005",
        #         "author": "Truyện cổ tích",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện về ba chú lợn con xây nhà.",
        #         "numberpage": 30,
        #         "form": "Bìa mềm",
        #         "size": "20x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837246/6f0f0cc4-0924-4262-9790-aae5f1240604.png",
        #         "price": 50000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Nàng Bạch Tuyết và bảy chú lùn",
        #         "productcode": "TN006",
        #         "author": "Truyện cổ tích Grimm",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện cổ tích nổi tiếng về nàng Bạch Tuyết.",
        #         "numberpage": 44,
        #         "form": "Bìa cứng",
        #         "size": "22x22 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837321/d7fc3a9e-0f00-429b-b974-89d38db09fec.png",
        #         "price": 60000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Alice ở xứ sở thần tiên",
        #         "productcode": "TN007",
        #         "author": "Lewis Carroll",
        #         "publisher": "NXB Kim Đồng",
        #         "description": "Câu chuyện phiêu lưu kỳ thú của Alice.",
        #         "numberpage": 120,
        #         "form": "Bìa mềm",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837400/7026dfef-17d3-4600-b994-2abeb21d7bf6.png",
        #         "price": 70000,
        #         "category_id": 1
        #     },
        #     {
        #         "name": "Hoàng tử bé",
        #         "productcode": "TN008",
        #         "author": "Antoine de Saint-Exupéry",
        #         "publisher": "NXB Trẻ",
        #         "description": "Tác phẩm kinh điển với nhiều bài học ý nghĩa.",
        #         "numberpage": 96,
        #         "form": "Bìa cứng",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837433/36ed2eb0-abe9-426f-a377-3cc782f11c02.png",
        #         "price": 85000,
        #         "category_id": 1
        #     },
        #
        #     # Tâm lý - Kỹ năng sống
        #     {
        #         "name": "Đắc Nhân Tâm",
        #         "productcode": "TL001",
        #         "author": "Dale Carnegie",
        #         "publisher": "NXB Trẻ",
        #         "description": "Cuốn sách giúp bạn xây dựng các mối quan hệ thành công.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "13x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837470/c1a131c8-3a48-4c56-a3b0-995d581043eb.png",
        #         "price": 120000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Quẳng gánh lo đi và vui sống",
        #         "productcode": "TL002",
        #         "author": "Dale Carnegie",
        #         "publisher": "NXB Trẻ",
        #         "description": "Bí quyết để có một cuộc sống an nhiên.",
        #         "numberpage": 280,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837530/bfb32a5c-eb26-49fb-a93d-78ec579ce585.png",
        #         "price": 110000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "7 Thói quen của bạn trẻ thành đạt",
        #         "productcode": "TL003",
        #         "author": "Sean Covey",
        #         "publisher": "NXB Trẻ",
        #         "description": "Thói quen giúp bạn trẻ đạt được thành công.",
        #         "numberpage": 350,
        #         "form": "Bìa mềm",
        #         "size": "13x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837568/c95a1627-a222-4824-8e51-868d14fb17ec.png",
        #         "price": 130000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Thiền Và Thực",
        #         "productcode": "TL004",
        #         "author": "Shunmyo Masuno",
        #         "publisher": "NXB Trẻ",
        #         "description": "Cách đơn giản hóa cuộc sống để đạt hạnh phúc.",
        #         "numberpage": 210,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837864/z3090981454074_8481377637fc109522f0dd857e2c3794_deuacv.jpg",
        #         "price": 115000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Tâm lý học hành vi",
        #         "productcode": "TL005",
        #         "author": "Edward Thorndike",
        #         "publisher": "NXB Lao Động",
        #         "description": "Khám phá tâm lý và hành vi con người.",
        #         "numberpage": 270,
        #         "form": "Bìa mềm",
        #         "size": "15x23 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837892/image_244718_1_1844_mxvshk.jpg",
        #         "price": 140000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Dám nghĩ lớn",
        #         "productcode": "TL006",
        #         "author": "David Schwartz",
        #         "publisher": "NXB Trẻ",
        #         "description": "Cách tư duy tích cực để đạt được mục tiêu lớn.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "13x20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734837956/vvvvvvvvvvvv_rfbmbj.webp",
        #         "price": 125000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Nghệ Thuật Tư Duy Rành Mạch",
        #         "productcode": "TL007",
        #         "author": "Rolf Dobelli",
        #         "publisher": "NXB Trẻ",
        #         "description": "Tránh các lỗi tư duy phổ biến trong cuộc sống.",
        #         "numberpage": 250,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734838045/nghe_thuat_tu_duy_ranh_mach_u2487_d20161129_t103616_398639_550x550_xrysjg.webp",
        #         "price": 135000,
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Kỹ năng giao tiếp đỉnh cao",
        #         "productcode": "TL008",
        #         "author": "Leil Lowndes",
        #         "publisher": "NXB Lao Động",
        #         "description": "Cách giao tiếp hiệu quả trong mọi tình huống.",
        #         "numberpage": 300,
        #         "form": "Bìa mềm",
        #         "size": "15x23 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734838076/image_195509_1_45380_ckqbu5.webp",
        #         "price": 150000,
        #         "category_id": 2
        #     },
        #     # Kinh tế
        #     {
        #         "name": "Kinh tế học",
        #         "productcode": "KT001",
        #         "author": "Paul A. Samuelson",
        #         "publisher": "NXB Kinh Tế",
        #         "description": "Cuốn sách kinh điển về kinh tế học cơ bản.",
        #         "numberpage": 500,
        #         "form": "Bìa cứng",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734838852/250f52e2-601b-435e-b17c-732723950ef5.png",
        #         "price": 200000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Tư bản",
        #         "productcode": "KT002",
        #         "author": "Karl Marx",
        #         "publisher": "NXB Chính Trị Quốc Gia",
        #         "description": "Tác phẩm kinh điển của kinh tế chính trị học.",
        #         "numberpage": 900,
        #         "form": "Bìa mềm",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734839324/image_222946_sijjkf.webp",
        #         "price": 250000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Kinh tế học vĩ mô",
        #         "productcode": "KT003",
        #         "author": "N. Gregory Mankiw",
        #         "publisher": "NXB Kinh Tế",
        #         "description": "Các nguyên lý cơ bản về kinh tế học vĩ mô.",
        #         "numberpage": 700,
        #         "form": "Bìa cứng",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734839355/9786044872643_1_c7tv8z.webp",
        #         "price": 300000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Chiến lược đại dương xanh",
        #         "productcode": "KT004",
        #         "author": "W. Chan Kim",
        #         "publisher": "NXB Trẻ",
        #         "description": "Chiến lược đổi mới sáng tạo.",
        #         "numberpage": 400,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734839418/image_219967_trgigh.webp",
        #         "price": 180000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Nền kinh tế chia sẻ",
        #         "productcode": "KT005",
        #         "author": "Arun Sundararajan",
        #         "publisher": "NXB Khoa Học",
        #         "description": "Khám phá về kinh tế chia sẻ trong thời đại mới.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "15x23 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734839460/nxbtre_full_05132018_031305_wyjqoy.webp",
        #         "price": 220000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Lý thuyết trò chơi",
        #         "productcode": "KT006",
        #         "author": "Trần Phách hàm",
        #         "publisher": "NXB Trẻ",
        #         "description": "Ứng dụng lý thuyết trò chơi trong kinh tế học.",
        #         "numberpage": 360,
        #         "form": "Bìa cứng",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734840172/8936066697088_w8w3up.webp",
        #         "price": 240000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Nghệ thuật thương thuyết",
        #         "productcode": "KT007",
        #         "author": "Chris Voss",
        #         "publisher": "Nhà Xuất Bản Tổng hợp TP.HCM",
        #         "description": "Bí quyết thương thuyết đỉnh cao.",
        #         "numberpage": 280,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734841414/nghe-thuat-thuong-thuyet-a.jpg_tz3ane.webp",
        #         "price": 200000,
        #         "category_id": 3
        #     },
        #     {
        #         "name": "Người Giàu Có Nhất Thành Babylon",
        #         "productcode": "KT008",
        #         "author": "George Samuel Clason",
        #         "publisher": "NXB Văn Học",
        #         "description": "Người Giàu Có Nhất Thành Babylon",
        #         "numberpage": 400,
        #         "form": "Bìa mềm",
        #         "size": "15x23 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734841565/a3ae47c0-8d87-4cd5-9473-6820d42d2300.png",
        #         "price": 230000,
        #         "category_id": 3
        #     },
        #
        #     # Văn học
        #     {
        #         "name": "Truyện Kiều",
        #         "productcode": "VH001",
        #         "author": "Nguyễn Du",
        #         "publisher": "NXB Văn Học",
        #         "description": "Tuyệt tác văn học cổ điển Việt Nam.",
        #         "numberpage": 220,
        #         "form": "Bìa cứng",
        #         "size": "15x22 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734841649/image_229223_gxhrt9.webp",
        #         "price": 150000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Những người khốn khổ",
        #         "productcode": "VH002",
        #         "author": "Victor Hugo",
        #         "publisher": "NXB Văn Học",
        #         "description": "Cuộc sống khổ cực của những con người bình dị.",
        #         "numberpage": 1300,
        #         "form": "Bìa mềm",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734841795/93f60d52e1f336c6ef6dd4d052347ed1.jpg_txg816.webp",
        #         "price": 350000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Chiến tranh và hòa bình",
        #         "productcode": "VH003",
        #         "author": "Lev Tolstoy",
        #         "publisher": "NXB Văn Học",
        #         "description": "Bức tranh toàn cảnh về chiến tranh và hòa bình.",
        #         "numberpage": 1400,
        #         "form": "Bìa cứng",
        #         "size": "16x24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734841954/a8933db5-a632-44d8-b023-6c416210f83e.png",
        #         "price": 400000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Nhà Giả Kim",
        #         "productcode": "VH004",
        #         "author": "Paulo Coelho",
        #         "publisher": "NXB Hội Nhà Văn",
        #         "description": "Tiểu thuyết Nhà giả kim của Paulo Coelho",
        #         "numberpage": 220,
        #         "form": "Bìa cứng",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734842077/image_195509_1_36793_m2ddie.webp",
        #         "price": 150000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Bản Chất Của Người (Tái Bản 2024)",
        #         "productcode": "VH005",
        #         "author": "Han Kang",
        #         "publisher": "NXB Hà Nội",
        #         "description": "Bản chất con người qua đôi mắt của Han Kang",
        #         "numberpage": 250,
        #         "form": "Bìa mềm",
        #         "size": "15x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734842604/ban-chat-cua-nguoi-01_k3kiql.webp",
        #         "price": 120000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Số đỏ",
        #         "productcode": "VH006",
        #         "author": "Vũ Trọng Phụng",
        #         "publisher": "NXB Văn Học",
        #         "description": "Cuốn tiểu thuyết trào phúng đặc sắc của Việt Nam.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734842608/so_do_hfu19w.webp",
        #         "price": 130000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Mắt biếc",
        #         "productcode": "VH007",
        #         "author": "Nguyễn Nhật Ánh",
        #         "publisher": "NXB Trẻ",
        #         "description": "Tác phẩm văn học nổi tiếng về tình yêu.",
        #         "numberpage": 400,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734842654/mat-biec_bia-mem_in-lan-thu-44_pail8f.webp",
        #         "price": 145000,
        #         "category_id": 4
        #     },
        #     {
        #         "name": "Chí Phèo",
        #         "productcode": "VH008",
        #         "author": "Nam Cao",
        #         "publisher": "NXB Văn Học",
        #         "description": "Tác phẩm văn học hiện thực phê phán đặc sắc.",
        #         "numberpage": 180,
        #         "form": "Bìa mềm",
        #         "size": "14x21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734842682/9786044916972_awvhyi.webp",
        #         "price": 120000,
        #         "category_id": 4
        #     },
        #     # Sách ngoại ngữ
        #     {
        #         "name": "Giáo Trình Chuẩn HSK 1 (Tái Bản 2023)",
        #         "productcode": "NN01",
        #         "author": "Khương Lệ Bình",
        #         "publisher": "NXB Tổng Hợp Thành Phố Hồ Chí Minh",
        #         "description": "Sách học tiếng Trung dành cho người mới bắt đầu, chuẩn bị cho kỳ thi HSK cấp 1.",
        #         "numberpage": 150,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734843870/9786043775662_nbnojj.webp",
        #         "price": 148500,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Giáo Trình Chuẩn HSK 1 - Sách Bài Tập (Tái Bản 2023)",
        #         "productcode": "NN02",
        #         "author": "Khương Lệ Bình",
        #         "publisher": "NXB Tổng Hợp Thành Phố Hồ Chí Minh",
        #         "description": "Sách bài tập bổ trợ cho Giáo Trình Chuẩn HSK 1, giúp củng cố kiến thức.",
        #         "numberpage": 120,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844272/9786045893104_mxehok.webp",
        #         "price": 118500,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Combo Sách Giáo Trình Chuẩn HSK 1 - Sách Bài Học Và Bài Tập (Bộ 2 Cuốn) (Tái Bản 2023)",
        #         "productcode": "NN03",
        #         "author": "Khương Lệ Bình",
        #         "publisher": "NXB Tổng Hợp Thành Phố Hồ Chí Minh",
        #         "description": "Bộ sách gồm sách bài học và bài tập, hỗ trợ học viên luyện thi HSK 1.",
        #         "numberpage": 270,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844337/51b92528-97f4-4150-a761-c6cff5a60d98_db4dx1.webp",
        #         "price": 261660,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "\"Chém\" Tiếng Anh Không Cần Động Não - Tặng Kèm Bộ Video Luyện Nghe-Nói + Sổ Học Từ Vựng",
        #         "productcode": "NN04",
        #         "author": "Bino",
        #         "publisher": "NXB Thế Giới",
        #         "description": "Sách hướng dẫn giao tiếp tiếng Anh một cách tự nhiên, kèm video luyện nghe-nói.",
        #         "numberpage": 200,
        #         "form": "Bìa mềm",
        #         "size": "14.5 x 20.5 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844377/chemta-bino_bia1_ahvunz.webp",
        #         "price": 126750,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Giáo Trình Chuẩn HSK 4 - Tập 1",
        #         "productcode": "NN05",
        #         "author": "Khương Lệ Bình",
        #         "publisher": "NXB Tổng Hợp Thành Phố Hồ Chí Minh",
        #         "description": "Sách học tiếng Trung dành cho trình độ trung cấp, chuẩn bị cho kỳ thi HSK cấp 4.",
        #         "numberpage": 180,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844457/image_230151_rffqro.webp",
        #         "price": 171000,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Tiếng Nhật Không Khó - Tiếng Nhật Cho Người Mới Học 2",
        #         "productcode": "NN06",
        #         "author": "Masateru Takatsu",
        #         "publisher": "NXB Tổng Hợp TPHCM",
        #         "description": "Sách dành cho giao tiếp và luyện thi chứng chỉ N5, N4.",
        #         "numberpage": 160,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844573/9786045864296_zsg6tc.webp",
        #         "price": 162000,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Kỳ Thi Năng Lực Tiếng Hàn Topik II - Thi Là Đậu",
        #         "productcode": "NN07",
        #         "author": "Hội nghiên cứu thi năng lực tiếng Hàn",
        #         "publisher": "NXB Trẻ",
        #         "description": "“TOPIK II - Thi là đậu” là giáo trình cập nhật mới nhất về kỳ thi và các dạng đề TOPIK II.",
        #         "numberpage": 150,
        #         "form": "Bìa mềm",
        #         "size": "19 x 27 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844723/image_220078_ysxve9.webp",
        #         "price": 340000,
        #         "category_id": 5
        #     },
        #     {
        #         "name": "Hacking Your English Speaking",
        #         "productcode": "NN08",
        #         "author": "Hoàng Ngọc Quỳnh",
        #         "publisher": "NXB Thế Giới",
        #         "description": "A practical guide to improve your English speaking skills effectively.",
        #         "numberpage": 220,
        #         "form": "Paperback",
        #         "size": "16 x 24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734844831/z5895072395093_970cadac9a946272b9670f43dd00f5ae_mpqxc3.webp",
        #         "price": 269000,
        #         "category_id": 5
        #     },
        #     # Sách thể loại khác
        #     {
        #         "name": "Chuyện Đời Chuyện Nghề",
        #         "productcode": "TL01",
        #         "author": "Võ Đắc Danh",
        #         "publisher": "NXB Hội Nhà Văn",
        #         "description": "Cuốn sách chia sẻ kinh nghiệm và bài học quý báu về nghề nghiệp và cuộc sống.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20.5 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734845933/9786043911107_rlf8nx.webp",
        #         "price": 460000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Hành Trình Về Phương Đông",
        #         "productcode": "TL02",
        #         "author": "Baird T. Spalding",
        #         "publisher": "NXB Hồng Đức",
        #         "description": "Tác phẩm kinh điển về hành trình tâm linh và cuộc sống.",
        #         "numberpage": 368,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20.5 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734845992/image_225174_kclnht.webp",
        #         "price": 99000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Chia Sẻ Từ Trái Tim (Thích Pháp Hòa)",
        #         "productcode": "TL03",
        #         "author": "Thích Pháp Hòa",
        #         "publisher": "NXB Dân Trí",
        #         "description": "Chia sẻ từ trái tim là một tuyển tập từ hàng trăm bài pháp thoại của Sa Môn Thích Pháp Hòa.",
        #         "numberpage": 250,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846154/c7666f54-142f-43eb-bc26-1126a7155d62.png",
        #         "price": 85000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Quẳng Gánh Lo Đi Và Vui Sống",
        #         "productcode": "TL04",
        #         "author": "Dale Carnegie",
        #         "publisher": "NXB Văn Học",
        #         "description": "Cuốn sách truyền cảm hứng, giúp người đọc vượt qua lo âu và sống hạnh phúc.",
        #         "numberpage": 320,
        #         "form": "Bìa mềm",
        #         "size": "15 x 21 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846192/9786043941555_vgxcjg.webp",
        #         "price": 120000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Sức Mạnh Tiềm Thức",
        #         "productcode": "TL05",
        #         "author": "Joseph Murphyc",
        #         "publisher": "NXB Tổng Hợp TPHCM",
        #         "description": "Cuốn sách hướng dẫn cách khai thác sức mạnh tiềm thức để đạt được thành công.",
        #         "numberpage": 288,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20.5 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846301/f0507c35-d74e-4fda-959f-e48df6b5084d.png",
        #         "price": 100000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Hạt Giống Tâm Hồn - Tập 16: Tìm Lại Bình Yên (Tái Bản 2023)",
        #         "productcode": "TL06",
        #         "author": "First News",
        #         "publisher": "NXB Tổng Hợp TPHCM",
        #         "description": "Tuyển tập các câu chuyện truyền cảm hứng về tình yêu, cuộc sống và hy vọng.",
        #         "numberpage": 250,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846405/3fbe80c6-acf3-41e2-8712-8deba3208ea0.png",
        #         "price": 85000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Muôn Kiếp Nhân Sinh",
        #         "productcode": "TL07",
        #         "author": "Nguyên Phong",
        #         "publisher": "NXB Tổng Hợp TP.HCM",
        #         "description": "Cuốn sách kể về những câu chuyện nhân sinh, khám phá quy luật luân hồi.",
        #         "numberpage": 400,
        #         "form": "Bìa mềm",
        #         "size": "16 x 24 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846463/68231911-ee31-4c91-9fba-d295ea8cbae9.png",
        #         "price": 200000,
        #         "category_id": 6
        #     },
        #     {
        #         "name": "Ánh Sáng Từ Trái Tim",
        #         "productcode": "TL08",
        #         "author": "Nguyễn Mỹ Trang",
        #         "publisher": "NXB Công Thương",
        #         "description": "Tuyển tập những câu chuyện cảm động, chạm đến trái tim người đọc.",
        #         "numberpage": 220,
        #         "form": "Bìa mềm",
        #         "size": "14 x 20 cm",
        #         "image": "https://res.cloudinary.com/duumdnwgx/image/upload/v1734846540/anh-sang-tu-trai-tim-bia-4_cbbd1w.webp",
        #         "price": 95000,
        #         "category_id": 6
        #     }
        # ]
        #
        # for p in data:
        #     prod = Product(
        #         name=p['name'] + ' ' + str(random.randint(1, 100)),  # Thêm số ngẫu nhiên vào tên
        #         productcode=p.get('productcode'),  # Dùng `get()` để tránh lỗi KeyError
        #         author=p.get('author'),
        #         publisher=p.get('publisher'),
        #         description=p['description'],
        #         numberpage=p.get('numberpage'),
        #         form=p.get('form'),
        #         size=p.get('size'),
        #         image=p['image'],
        #         price=p['price'],
        #         category_id=p['category_id']
        #     )
        #     db.session.add(prod)
        #
        # db.session.commit()
