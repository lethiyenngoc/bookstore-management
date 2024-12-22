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
    fetch(`/api/products/${productId}/comments`, {
        method: 'post',
        body: JSON.stringify({
            'content': document.getElementById("comment").value
        }),
         headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(c => {
        let html = `
        <li class="list-group-item">
            <div class="row">
                <div class="col-md-1 col-4">
                    <img src="${ c.user.avatar }" class="img-fluid rounded-circle" />
                </div>
                <div class="col-md-11 col-8">
                    <p>${ c.content }</p>
                    <p class="date">${ moment(c.created_date).locale("vi").fromNow() }</p>
                </div>
            </div>
        </li>
        `;

        let comments = document.getElementById("comments");
        comments.innerHTML = html + comments.innerHTML;
    })
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