$(function () {
    let isSearched = false;
    const userId = $("#userId").text();
    let keyword;

    let skip = 0;
    const take = 10;

    let body = {
        user_id: userId,
        keyword: keyword,
        skip: skip,
        take: take,
    };
    let total = -1;

    $("#searchButton").click(function (_) {
        keyword = $("#searchTextbox").val();
        body["keyword"] = keyword;
        $.post("search", JSON.stringify(body))
            .done(function (data) {
                isSearched = true;
                $("#searchResult > .results").html(data);
                $("#searchResult").show();
                total = parseInt($(".total").last().text());
            })
            .fail(function (error) {
                console.error(error);
            });
    });

    function addNewResults() {
        skip += take;
        body["skip"] = skip;

        $.post("search", JSON.stringify(body))
            .done(function (data) {
                $("#searchResult > .results").append(data);
                total = parseInt($(".total").last().text());
            })
            .fail(function (error) {
                console.error(error);
            });
    }

    window.onscroll = function () {
        if (
            !isSearched ||
            skip + take >= total ||
            getScrollTop() < getDocumentHeight() - window.innerHeight
        ) {
            return;
        }

        addNewResults();
    };
});

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
