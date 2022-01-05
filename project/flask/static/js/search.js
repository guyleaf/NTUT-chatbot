$(function () {
  let isSearched = false;
  let keyword;

  const spinner = new Spin.Spinner().spin();

  const take = 10;

  let requestBody = {
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

    $.ajax({
      type: "POST",
      url: "/products/search",
      headers: {
        'X-CSRF-TOKEN': getCsrfToken()
      },
      data: JSON.stringify(requestBody),
      contentType: "application/json; charset=UTF-8"
    })
      .done(function (data, _, xhr) {
        let contentType = xhr.getResponseHeader("Content-Type");

        if (contentType === "application/json") {
          handleJsonResponse(data)
        }
        else {
          $("#searchResult > .results").html(data);

          total = getTotal();
          if (total === 0) {
            $("#resultsNotFoundMessage").show();
          }

          // setupFavoriteFunction(userId);
          isSearched = true;
        }
      })
      .fail(handleErrorResponse);
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

    $.ajax({
      type: "POST",
      url: "/products/search",
      headers: {
        'X-CSRF-TOKEN': getCsrfToken()
      },
      data: JSON.stringify(requestBody),
      contentType: "application/json; charset=UTF-8",
      dataType: "html"
    })
      .done(function (data, _, xhr) {
        let contentType = xhr.getResponseHeader("Content-Type");

        if (contentType === "application/json") {
          handleJsonResponse(data)
        }
        else {
          $("#searchResult > .results").append(data);
          total = getTotal();
        }
      })
      .fail(handleErrorResponse);
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
