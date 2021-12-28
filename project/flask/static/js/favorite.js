function setupFavoriteFunction(userId, callbackForAdd, callbackForDelete) {
    setupAddFavoriteFunction(userId, callbackForAdd);
    setupDeleteFavoriteFunction(userId, callbackForDelete);
}

function setupAddFavoriteFunction(userId, callback) {
    let addFavoriteModal = new bootstrap.Modal(
        document.getElementById("addFavoriteSuccessHint")
    );
    $(".addFavoriteButton").click(function (e) {
        e.preventDefault();
        const productId = $(e.target).data("product-id");
        $.post(
            "/" + userId + "/myFavorites",
            JSON.stringify({ product_id: productId })
        )
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

function setupDeleteFavoriteFunction(userId, callback) {
    let deleteFavoriteModal = new bootstrap.Modal(
        document.getElementById("deleteFavoriteSuccessHint")
    );
    $(".deleteFavoriteButton").click(function (e) {
        e.preventDefault();
        const productId = $(e.target).data("product-id");
        $.ajax({
            url: "/" + userId + "/myFavorites",
            type: "DELETE",
            data: JSON.stringify({ product_id: productId }),
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
