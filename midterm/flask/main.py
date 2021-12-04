from flask import Flask, render_template, url_for, request, redirect, jsonify
import firestoreDAO
import json
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
#@app.route('/myFavorite/<userId>', methods=['GET'])
@app.route('/myFavorite', methods=['GET'])
def myFavorite(userId):
    title = "我的最愛"
    myFavorites = firestoreDAO.getFavorites(userId)
    return render_template("myFavorite.html", **locals())

@app.route('setFavorite',methods=['POST'])
def setFavorite(userId, productInfo):
    #process productInfo
    response = {
        "id": productInfo["id"],
        "name": productInfo["name"],
        "brand": productInfo["brand"],
        "price": productInfo["price"],
        "quantity": productInfo["quantity"],
    }
    firestoreDAO.setFavorites(userId, response)
    return jsonify('加入最愛成功')

#buyer state:-1 處理中, 0 運送中 , 1已完成
#@app.route('/orderRecord/<userId>', methods=['GET', 'POST'])
@app.route('/orderRecord', methods=['GET', 'POST'])
def orderRecord(userId):
    title = "訂單紀錄"
    orders = firestoreDAO.getOrder(userId)
    return render_template("orderRecord.html", **locals())

@app.route('/updateOrder', methods=['POST'])
def updateOrder(userId, orderInfo):
    title = "訂單紀錄"
    orders = firestoreDAO.updateOrder(userId, orderInfo)
    return jsonify('更新訂單成功')

@app.route('/addOrder', methods=['POST'])
def addOrder(userId, orderInfo):
    title = "訂單紀錄"
    orders = firestoreDAO.addOrder(userId, orderInfo)
    return jsonify('新增訂單成功')


#seller
#@app.route('/stockManagement/<userId>', methods=['GET', 'POST'])
@app.route('/stockManagement', methods=['GET'])
def stockManagement(userId):
    title = "商品管理"
    produtcts = firestoreDAO.getProducts(userId)
    return render_template("stockManagement.html", **locals())


#seller
#@app.route('/orderManagement/<userId>', methods=['GET', 'POST'])
@app.route('/orderManagement', methods=['GET'])
def orderManagement(userId):
    title = "訂單管理"
    orders = firestoreDAO.getOrder(userId)
    return render_template("orderManagement.html", **locals())



if __name__ == "__main__":
    app.run(debug=True)