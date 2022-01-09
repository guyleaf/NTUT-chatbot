$(function () {
  const form = $("#productForm");
  form.submit(function (event) {
    if (!form[0].checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }

    form.addClass("was-validated");
  });


  $("#deleteButton").click(function (e) {
    e.preventDefault();

    const returnUrl = $(e.target).data("return-url");
    const productId = $(e.target).data("product-id");

    window.helpers.ajax("DELETE", `/products/${productId}`, JSON.stringify({}))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);

        window.location.href = returnUrl;
      })
      .fail(window.helpers.handleErrorResponse);
  });
})
