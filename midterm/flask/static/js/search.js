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

    $("#searchButton").click(function (e) {
        e.preventDefault();
        keyword = $("#searchTextbox").val();
        body["keyword"] = keyword;
        $.post("search", JSON.stringify(body))
            .done(function (data) {
                $("#searchResult > .results").html(data);
                $("#searchResult").show();
                total = parseInt($(".total").last().text());
                if (!isSearched) {
                    setup(userId);
                }
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
        scrollFunction("#scrollToTopButton");
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

function setup(userId) {
    let addFavoriteModal = new bootstrap.Modal(
        document.getElementById("addFavoriteSuccessHint")
    );
    let deleteFavoriteModal = new bootstrap.Modal(
        document.getElementById("deleteFavoriteSuccessHint")
    );

    $(".purchaseButton").click(function (e) {
        e.preventDefault();
    });
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
