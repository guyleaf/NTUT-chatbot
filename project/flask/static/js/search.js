$(function () {
  let isSearched = false;
  const userId = $("#userId").text();
  let keyword;

  const spinner = new Spin.Spinner().spin();

  const take = 10;

  let requestBody = {
    user_id: userId,
    keyword: keyword,
    skip: 0,
    take: take,
  };
  let total = -1;

  $("#searchForm").submit(function (e) {
    e.preventDefault();
    reset();
    $("#searchResult").show();
    $("#resultsNotFoundMessage").hide();
    $("#searchResult > .results").html(spinner.el);

    keyword = $("#searchTextbox").val();
    requestBody["keyword"] = keyword;

    $.post("search", JSON.stringify(requestBody))
      .done(function (data) {
        $("#searchResult > .results").html(data);

        total = getTotal();
        if (total === 0) {
          $("#resultsNotFoundMessage").show();
        }

        setupFavoriteFunction(userId);
        isSearched = true;
      })
      .fail(function (error) {
        console.error(error);
      });
  });

  $("#scrollToTopButton").click(function (e) {
    e.preventDefault();
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  });

  function reset() {
    requestBody["skip"] = 0;
    isSearched = false;
  }

  function addNewResults() {
    requestBody["skip"] += take;
    $.post("search", JSON.stringify(requestBody))
      .done(function (data) {
        $("#searchResult > .results").append(data);
        total = getTotal();
      })
      .fail(function (error) {
        console.error(error);
      });
  }

  function getTotal() {
    return parseInt($(".total").last().text());
  }

  function scrollFunction(target) {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      $(target).show();
    } else {
      $(target).hide();
    }
  }

  function getDocumentHeight() {
    const body = document.body;
    const html = document.documentElement;

    return Math.max(
      body.scrollHeight,
      body.offsetHeight,
      html.clientHeight,
      html.scrollHeight,
      html.offsetHeight
    );
  }

  function getScrollTop() {
    return window.pageYOffset !== undefined
      ? window.pageYOffset
      : (
        document.documentElement ||
        document.body.parentNode ||
        document.body
      ).scrollTop;
  }

  window.onscroll = function () {
    scrollFunction("#scrollToTopButton");
    if (
      !isSearched ||
      requestBody["skip"] + take >= total ||
      getScrollTop() < getDocumentHeight() - window.innerHeight
    ) {
      return;
    }

    addNewResults();
  };
});
