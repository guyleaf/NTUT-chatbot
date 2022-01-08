$(function () {
  const form = $("#product_form");
  form.submit(function (event) {
    if (!form[0].checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }

    form.addClass("was-validated");
  });

  const returnUrl = $("#returnUrl").text();
  const productUrl = $("#product_url").text();
  $("#deleteButton").click(function (e) {
    e.preventDefault();

    window.helpers.ajax("DELETE", productUrl, JSON.stringify({}))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);
        console.log(data);
        window.location.href = returnUrl;
      })
      .fail(window.helpers.handleErrorResponse);
  });
})
