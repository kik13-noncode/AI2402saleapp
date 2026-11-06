import math

from flask import render_template, request, redirect, session

from eapp import app, dao, login, utils
from flask_login import login_user
from flask_login import logout_user


@app.route("/")
def index():
    count = dao.count_products()
    page_size = app.config['PAGE_SIZE']
    products = dao.load_products(kw=request.args.get('kw'), cate_id=request.args.get('category_id'), page=int(request.args.get('page',1)))
    return render_template('index.html', products=products, page= math.ceil(count/page_size))

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.authorize(username= username, password= password)
    if u :
        login_user(user=u)

    return redirect('/') if request.args.get('from') else redirect('/admin')

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/logout')
def logout_view():
    logout_user()
    return redirect('/login')


@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    msg =''
    if not password or not confirm or password != confirm:
        msg = 'Mật khẩu không khớp!'
    else:
        data = request.form.copy()
        del data['confirm']

        data['avatar'] = request.files.get('avatar')
        dao.add_user(**data)
        return redirect('/login')
    return render_template('register.html', msg=msg)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/api/cart', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart={}
    id = request.json.get('id')

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': 1,
            'name': request.json.get('name'),
            'price': request.json.get('price'),
            'quantity': 1
        }
    session['cart'] = cart
    print(cart)

@app.route('/api/cart/<product_id>', methods=['patch'])
def update_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json.get('quantity', cart[product_id]['quantity']))
    session['cart'] = cart
    return utils.count_cart(cart=cart)


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
       del cart[product_id]
    session['cart'] = cart
    return utils.count_cart(cart=cart)
'''
{
    '1': {
        'id': 1,
        'name': 'abc'
        'price': 123,
        'quantity': 2
    },
    '2': {
        'id': 2,
        'name': 'abc'
        'price': 123,
        'quantity':1
    }
}
'''


@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories(),
        'carts': utils.count_cart(session.get('cart'))
    }
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    with app.app_context():
        from eapp import admin
        app.run(debug=True)
