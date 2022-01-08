function setupFavoriteFunction(addButtonTarget, removeButtonTarget, callbackForAdd, callbackForDelete) {
  unbindFavoriteFunction(addButtonTarget, removeButtonTarget);
  setupAddFavoriteFunction(addButtonTarget, removeButtonTarget, callbackForAdd);
  setupDeleteFavoriteFunction(addButtonTarget, removeButtonTarget, callbackForDelete);
}

function unbindFavoriteFunction(addButtonTarget, removeButtonTarget) {
  const eventName = "click";
  window.helpers.unbindEvent(addButtonTarget, eventName);
  window.helpers.unbindEvent(removeButtonTarget, eventName);
}

function setupAddFavoriteFunction(addButtonTarget, removeButtonTarget, callback) {
  let addFavoriteModal = new bootstrap.Modal(
    document.getElementById("addFavoriteSuccessHint")
  );
  $(addButtonTarget).click(function (e) {
    e.preventDefault();
    const productId = $(e.target).data("product-id");
    window.helpers.ajax("POST", "/myFavorites", JSON.stringify({ product_id: productId }))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);
        $(e.target).hide();
        $(e.target).siblings(removeButtonTarget).show();
        addFavoriteModal.show();
      })
      .fail(function (error) {
        window.helpers.handleErrorResponse(error);
      });
  });

  _addEventListenersForClosed("addFavoriteSuccessHint", callback);
}

function setupDeleteFavoriteFunction(addButtonTarget, removeButtonTarget, callback) {
  let deleteFavoriteModal = new bootstrap.Modal(
    document.getElementById("deleteFavoriteSuccessHint")
  );
  $(removeButtonTarget).click(function (e) {
    e.preventDefault();
    const productId = $(e.target).data("product-id");
    window.helpers.ajax("DELETE", "/myFavorites", JSON.stringify({ product_id: productId }))
      .done(function (data) {
        window.helpers.handleJsonResponse(data);

        $(e.target).hide();
        $(e.target).siblings(addButtonTarget).show();
        deleteFavoriteModal.show();
      })
      .fail(function (error) {
        window.helpers.handleErrorResponse(error);
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
