$(function () {
    const userId = $("#userId").text();
    console.log(userId);
    const callbackForDelete = function () {
        location.reload();
    };
    setupDeleteFavoriteFunction(userId, callbackForDelete);
});
