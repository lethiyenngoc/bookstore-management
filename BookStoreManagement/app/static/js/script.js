function addToCart(id, name, price) {
    fetch('/api/carts', {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        let counters = document.getElementsByClassName("cart-counter");
        for (let c of counters)
            c.innerText = data.total_quantity;
    })
}

//window.onload = function() {
//    let buttons = document.getElementsByClassName("booking");
//    for (let b of buttons)
//        b.onclick = function() {
//
//        }
//}