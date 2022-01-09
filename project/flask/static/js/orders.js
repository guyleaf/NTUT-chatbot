$(function () {
  $("#orderTable").find("button").click(function (e) {
    target = $(e.target);

    const orderId = target.data("order-id");
    const value = target.data("value");
    console.log(orderId, value);
    window.helpers.ajax("PUT", `/orders/${orderId}`, JSON.stringify({ status_id: value }))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);

        window.location.reload();
      })
      .fail(window.helpers.handleErrorResponse);
  })
})