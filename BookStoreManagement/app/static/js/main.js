function updateUI(data) {
    let items = document.getElementsByClassName("cart-counter");
    for (let item of items)
        item.innerText = data.total_quantity;

    let amounts = document.getElementsByClassName("cart-amount");
    for (let item of amounts)
        item.innerText = data.total_amount.toLocaleString();
}

function addToCart(id, name, price) {
    fetch("/api/carts", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
       updateUI(data);
    })
}

function updateCart(productId, obj) {
    fetch(`/api/carts/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        updateUI(data);
    })
}

function deleteCart(productId) {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
         fetch(`/api/carts/${productId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            updateUI(data);
            document.getElementById(`cart${productId}`).style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
         fetch(`/api/pay`, {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                location.reload();
            }
        });
    }
}

function addComment(productId) {
    const rating = document.getElementById("rating")?.value || 5;
    const content = document.getElementById("comment").value;

    if (!content.trim()) {
        alert("Nội dung bình luận không được để trống!");
        return;
    }

    fetch(`/api/products/${productId}/comments`, {
        method: 'post',
        body: JSON.stringify({
            content: content,
            rating: rating
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => {
                throw new Error(err.error || 'Đã xảy ra lỗi khi thêm bình luận!');
            });
        }
        return res.json();
    })
    .then(c => {
        const avatar = c.user.avatar || '/static/images/default-avatar.png';
        const userName = c.user.name || "Anonymous";

        // Sử dụng Moment.js để định dạng thời gian
        const relativeTime = moment(c.created_date).locale("vi").fromNow();

        // Tạo HTML hiển thị số sao đánh giá
        let starsHtml = '';
        for (let i = 1; i <= 5; i++) {
            starsHtml += i <= c.rating
                ? '<span class="text-warning">&#9733;</span>' // Sao vàng
                : '<span class="text-muted">&#9733;</span>'; // Sao xám
        }

        const html = `
        <li class="list-group-item">
            <div class="row">
                <div class="col-md-1 col-4">
                    <img src="${avatar}" class="img-fluid rounded-circle" />
                </div>
                <div class="col-md-11 col-8">
                    <strong>${userName}</strong>
                    <p>${c.content}</p>
                    <p>${starsHtml}</p> <!-- Hiển thị đánh giá sao -->
                    <p class="date">${relativeTime}</p> <!-- Hiển thị thời gian tương đối -->
                </div>
            </div>
        </li>
        `;

        const comments = document.getElementById("comments");
        comments.innerHTML = html + comments.innerHTML;

        // Xóa nội dung trong ô nhập bình luận
        document.getElementById("comment").value = "";
    })
    .catch(err => {
        alert(err.message);
        console.error('Failed to add comment:', err);
    });
}


//window.onload = function() {
//    let buttons = document.getElementsByClassName("booking");
//    for (let b of buttons)
//        b.onclick = function() {
//
//        }
//}

  document.getElementById('decrease-quantity').addEventListener('click', () => {
    const quantityInput = document.getElementById('quantity');
    let quantity = parseInt(quantityInput.value);
    if (quantity > 1) {
      quantityInput.value = quantity - 1;
    }
  });

  document.getElementById('increase-quantity').addEventListener('click', () => {
    const quantityInput = document.getElementById('quantity');
    let quantity = parseInt(quantityInput.value);
    quantityInput.value = quantity + 1;
  });

  // Zoom effect logic
  const zoomContainer = document.querySelector('.image-zoom-container');
  const zoomImage = document.querySelector('.image-zoom');
  const magnifier = document.querySelector('.magnifier');

  zoomContainer.addEventListener('mousemove', (e) => {
    const rect = zoomContainer.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const zoomFactor = 2; // Độ phóng to
    zoomImage.style.transform = `scale(${zoomFactor})`;

    const bgPosX = -(x * (zoomFactor - 1)) + 'px';
    const bgPosY = -(y * (zoomFactor - 1)) + 'px';

    magnifier.style.visibility = 'visible';
    magnifier.style.left = `${x - magnifier.offsetWidth / 2}px`;
    magnifier.style.top = `${y - magnifier.offsetHeight / 2}px`;
    magnifier.style.backgroundImage = `url(${zoomImage.src})`;
    magnifier.style.backgroundSize = `${zoomImage.width * zoomFactor}px ${zoomImage.height * zoomFactor}px`;
    magnifier.style.backgroundPosition = `${bgPosX} ${bgPosY}`;
  });

  zoomContainer.addEventListener('mouseleave', () => {
    zoomImage.style.transform = 'scale(1)';
    magnifier.style.visibility = 'hidden';
  });