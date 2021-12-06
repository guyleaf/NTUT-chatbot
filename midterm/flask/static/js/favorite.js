function setupFavoriteFunction(userId) {
    let addFavoriteModal = new bootstrap.Modal(
        document.getElementById("addFavoriteSuccessHint")
    );
    let deleteFavoriteModal = new bootstrap.Modal(
        document.getElementById("deleteFavoriteSuccessHint")
    );
    $(".deleteFavoriteButton").click(function (e) {
        e.preventDefault();
        const productId = $(e.target).data("product-id");
        $.ajax({
            url: userId + "/myFavorites",
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
    $(".addFavoriteButton").click(function (e) {
        e.preventDefault();
        const productId = $(e.target).data("product-id");
        $.post(
            userId + "/myFavorites",
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
}
