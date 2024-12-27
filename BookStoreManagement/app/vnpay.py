import hashlib
import hmac
import urllib.parse

def create_vnpay_url(order_id, total_amount, return_url):
    vnp_url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    tmn_code = "LUS0AQO2"
    secret_key = "4S5PEP19803HUJBCDHV44JRNNMQ55MQL"

    # Dữ liệu thanh toán
    data = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": total_amount * 100,  # Số tiền tính theo VNĐ x100
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": order_id,
        "vnp_OrderInfo": f"Thanh toán đơn hàng {order_id}",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": return_url,
        "vnp_IpAddr": "127.0.0.1",
    }

    # Sắp xếp dữ liệu theo key tăng dần
    sorted_data = sorted(data.items())
    query_string = "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_data])

    # Tạo chữ ký
    hash_data = hmac.new(
        bytes(secret_key, "utf-8"),
        bytes(query_string, "utf-8"),
        hashlib.sha512,
    ).hexdigest()

    # Tạo URL thanh toán
    payment_url = f"{vnp_url}?{query_string}&vnp_SecureHash={hash_data}"
    return payment_url
