import math

from flask import render_template, request

from eapp import app, dao


@app.route("/")
def index():
    count = dao.count_products()
    page_size = app.config['PAGE_SIZE']
    products = dao.load_products(kw=request.args.get('kw'), cate_id=request.args.get('category_id'), page=int(request.args.get('page',1)))
    return render_template('index.html', products=products, page= math.ceil(count/page_size))

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories()
    }

if __name__ == '__main__':
    with app.app_context():
        from eapp import admin
        app.run(debug=True)