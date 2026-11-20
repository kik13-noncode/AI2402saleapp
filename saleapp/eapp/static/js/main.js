function addToCart(id, name, price) {
    fetch('/api/cart', {
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
        let eles = document.getElementsByClassName('cart-counter');
        for (let e of eles)
            e.innerText = data.total_quantity;
    })
}

function updateCart(id, obj) {
    fetch(`/api/cart/${id}`, {
        method: "patch",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let eles = document.getElementsByClassName('cart-counter');
        for (let e of eles)
            e.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName('cart-amount');
        for (let e of amounts)
            e.innerText = data.total_amount.toLocaleString('en');
    })
}

function deleteCart(id) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let m = document.getElementById(`cart${id}`);
            m.style.display = 'none';

            let eles = document.getElementsByClassName('cart-counter');
            for (let e of eles)
                e.innerText = data.total_quantity;

            let amounts = document.getElementsByClassName('cart-amount');
            for (let e of amounts)
                e.innerText = data.total_amount.toLocaleString('en');
        })
    }
}
