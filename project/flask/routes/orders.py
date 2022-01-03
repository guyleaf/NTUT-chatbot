# buyer state:-1 處理中, 0 運送中 , 1已完成
@app.route("/<user_id>/orders", methods=["GET"])
def get_order_page(user_id):
    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "我的最愛"
    orders = firestoreDAO.get_orders(user_id)
    return render_template(
        "orderRecord.html", title=title, orders=orders, user_id=user_id
    )


@app.route("/<user_id>/orders", methods=["PUT"])  # Ron wrote
def update_order(user_id):
    body = request.get_json(force=True)
    errors = update_order_action_schema.validate(body)  # Don't know how to do

    if errors:
        return errors, 400

    body = update_order_action_schema.load(body)  # Don't know how to do

    order_id = body["order_id"]
    state = body["state"]
    order_info = {"id": order_id, "state": state}  # state:-1 處理中, 0 運送中 , 1已完成

    if not firestoreDAO.is_order_existed(order_id):
        return {
            "success": False,
            "message": order_not_found_message_for_api,
        }, 404
    if not firestoreDAO.is_user_exists_by_id(user_id):
        return {
            "success": False,
            "message": user_not_found_message_for_api,
        }, 404

    firestoreDAO.update_order(user_id, order_info)
    return jsonify("更新訂單成功")


@app.route("/<user_id>/orders", methods=["POST"])  # Ron wrote
def add_order(user_id):
    body = request.get_json(force=True)
    errors = add_order_action_schema.validate(body)  # Don't know how to do

    if errors:
        return errors, 400

    body = add_order_action_schema.load(body)  # Don't know how to do

    product_id = body["product_id"]
    quantity = body["quantity"]
    order_info = {
        "product_id": product_id,
        "quantity": quantity,
        "state": -1,  # state:-1 處理中, 0 運送中 , 1已完成
    }

    if not firestoreDAO.is_product_existed(product_id):
        return {
            "success": False,
            "message": product_not_found_message_for_api,
        }, 404
    if not firestoreDAO.is_user_exists_by_id(user_id):
        return {
            "success": False,
            "message": user_not_found_message_for_api,
        }, 404

    firestoreDAO.add_order(user_id, order_info)
    return jsonify("新增訂單成功")


# seller
@app.route("/<user_id>/orders", methods=["GET"])
def manage_orders(user_id):
    title = "訂單管理"
    orders = firestoreDAO.get_orders(user_id)
    return render_template("orderManagement.html", **locals())
