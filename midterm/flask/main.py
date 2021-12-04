from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    title = "HOME"
    #if request.method == 'POST' and "search_result" in request.form.get("website"):
    #    return redirect(url_for(search_result, keyword="123"))
    if request.method == 'POST':
        return redirect(url_for(request.form.get("website")))
    return render_template('home.html', **locals())

#both
@app.route('/search_page', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        return redirect(url_for('search_result/', keyword=request.form.get("keyword")))
    else:
        title = "搜尋商品"
        return render_template("search_page.html", **locals())

#both
@app.route('/search_result/', methods=['GET', 'POST'])
def search_result():
    title = "商品列表"
    if request.method == 'POST':
        return redirect(url_for('search_result', keyword=request.form.get("keyword")))
    else:
        response = {
            "products":[
                {
                    "name":"3080",
                    "brand":"ASUS",
                    "price": 1000,
                    "quantity": 5,
                    "imgSrc": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg"
                },
                {
                    "name":"3070",
                    "brand":"ROG",
                    "price": 800,
                    "quantity": 0,
                    "imgSrc":"https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9"
                },
                {
                    "name":"3060",
                    "brand":"ZOTAC",
                    "price": 600,
                    "quantity": 3,
                    "imgSrc":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZClI_bI7QUEtyZmPZs_VTx-DzQts0ScIs-g&usqp=CAU"
                }
            ]
        }
    return render_template("search_result.html", **locals())

#both
#@app.route('/favorite/<memberId>', methods=['GET', 'POST'])
@app.route('/myFavorite', methods=['GET', 'POST'])
def favorite():
    title = "我的最愛"
    response = {
            "products":[
                {
                    "name":"3080",
                    "brand":"ASUS",
                    "price": 1000,
                    "quantity": 5,
                    "imgSrc": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg"
                },
                {
                    "name":"3070",
                    "brand":"ROG",
                    "price": 800,
                    "quantity": 0,
                    "imgSrc":"https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9"
                }
            ]
    }
    return render_template("myFavorite.html", **locals())

#seller
#@app.route('/stockManagement/<memberId>', methods=['GET', 'POST'])
@app.route('/stockManagement', methods=['GET', 'POST'])
def stock():
    title = "商品管理"
    response = {
            "products":[
                {
                    "name":"3080",
                    "brand":"ASUS",
                    "price": 1000,
                    "quantity": 5,
                    "onShelf" : 1,
                    "imgSrc": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg"
                },
                {
                    "name":"3070",
                    "brand":"ROG",
                    "price": 800,
                    "quantity": 0,
                    "onShelf" : 0,
                    "imgSrc":"https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9"
                }
            ]
    }
    return render_template("stockManagement.html", **locals())

#@app.route('/record/<memberId>', methods=['GET', 'POST'])
@app.route('/orderRecord', methods=['GET', 'POST'])
def record():
    title = "訂單紀錄"
    response = {
            "records":[
                {
                    "index": 1,
                    "name":"3080",
                    "brand":"ASUS",
                    "price": 1000,
                    "quantity": 5,
                    "date": "11/27",
                    "imgSrc": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg"
                },
                {
                    "index": 2,
                    "name":"3070",
                    "brand":"ROG",
                    "price": 800,
                    "quantity": 1,
                    "date": "12/01",
                    "imgSrc":"https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9"
                }
            ]
    }
    return render_template("record.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)