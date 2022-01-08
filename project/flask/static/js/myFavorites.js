$(function () {
  const callbackForDelete = function () {
    location.reload();
  };
  setupDeleteFavoriteFunction(".addFavoriteButton", ".deleteFavoriteButton", callbackForDelete);
});
