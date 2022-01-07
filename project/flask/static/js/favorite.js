function setupFavoriteFunction(callbackForAdd, callbackForDelete) {
  setupAddFavoriteFunction(callbackForAdd);
  setupDeleteFavoriteFunction(callbackForDelete);
}

function setupAddFavoriteFunction(callback) {
  let addFavoriteModal = new bootstrap.Modal(
    document.getElementById("addFavoriteSuccessHint")
  );
  $(".addFavoriteButton").click(function (e) {
    e.preventDefault();
    const productId = $(e.target).data("product-id");
    $.ajax({
      type: "POST",
      url: "/myFavorites",
      headers: {
        'X-CSRF-TOKEN': getCsrfToken()
      },
      data: JSON.stringify({ product_id: productId }),
      contentType: "application/json; charset=UTF-8"
    })
      .done(function (_) {
        console.log("success");
        $(e.target).hide();
        $(e.target).siblings(".deleteFavoriteButton").show();
        addFavoriteModal.show();
      })
      .fail(function (error) {
        console.error(error);
      });
  });

  _addEventListenersForClosed("addFavoriteSuccessHint", callback);
}

function setupDeleteFavoriteFunction(callback) {
  let deleteFavoriteModal = new bootstrap.Modal(
    document.getElementById("deleteFavoriteSuccessHint")
  );
  $(".deleteFavoriteButton").click(function (e) {
    e.preventDefault();
    const productId = $(e.target).data("product-id");
    $.ajax({
      type: "DELETE",
      url: "/myFavorites",
      headers: {
        'X-CSRF-TOKEN': getCsrfToken()
      },
      data: JSON.stringify({ product_id: productId }),
      contentType: "application/json; charset=UTF-8"
    })
      .done(function (_) {
        console.log("success");
        $(e.target).hide();
        $(e.target).siblings(".addFavoriteButton").show();
        deleteFavoriteModal.show();
      })
      .fail(function (error) {
        console.error(error);
      });
  });

  _addEventListenersForClosed("deleteFavoriteSuccessHint", callback);
}

function _addEventListenersForClosed(target, callback) {
  const modal = document.getElementById(target);
  modal.addEventListener("hidden.bs.modal", function (e) {
    if (callback) {
      callback();
    }
  });
}
