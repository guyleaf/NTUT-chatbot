$(function () {
  const form = $("#product_form");
  form.submit(function (event) {
    if (!form[0].checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }

    form.addClass("was-validated");
  });

  const product_url = $("#product_url").val();
  $("#deleteButton").click(function (e) {
    e.preventDefault();
    window.helpers.ajax("DELETE", product_url, JSON.stringify({}))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);

        window.location.replace("/products/search");
      })
      .fail(window.helpers.handleErrorResponse);
  });
})
