from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/search_result', methods=['GET', 'POST'])
def search_result():
    title = "商品列表"
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
    return render_template("search_result.html",**locals())

if __name__ == "__main__":
    app.run(debug=True)