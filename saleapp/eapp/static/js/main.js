function addToCart(id, name, price){
    fetch('/api/cart',{
        method: "post",
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        header: {
            'Content-Type': 'application/json'
        }
    }).then(res =>res.json()).then(data =>{
        let eles = document.getElementsByClassName('cart-counter');
        for(let e of eles)
            e.innerText = data.total_quantity;
    })
}

function updateCart(id, obj){
    fetch('/api/cart/${id}',{
        method: "post",
        body: JSON.stringify({

            'price': obj.value
        }),
        header: {
            'Content-Type': 'application/json'
        }
    }).then(res =>res.json()).then(data =>{
        let eles = document.getElementsByClassName('cart-counter');
        for(let e of eles)
            e.innerText = data.total_quantity;

        let amount = document.getElementsByClassName('cart-amount');
        for(let e of amounts)
            e.innerText = data.total_amount.toLocalString('en');
    })

}

function deleteCart(){
    if (confirm("bạn chắc chắn xóa không?") == true)
    fetch('/api/cart/${id}',{
        method: "delete"
    }).then(res =>res.json()).then(data =>{
        let m = document.getElementById(`cart${id}`)
        m.style.display = 'name';

        let eles = document.getElementsByClassName('cart-counter');
        for(let e of eles)
            e.innerText = data.total_quantity;

        let amount = document.getElementsByClassName('cart-amount');
        for(let e of amounts)
            e.innerText = data.total_amount.toLocalString('en');
    })
}
