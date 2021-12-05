$(function () {
    $("#searchButton").click(function (_) {
        const userId = $("#userId").text();
        const keyword = $("#searchTextbox").val();
        const body = {
            user_id: userId,
            keyword: keyword,
            skip: 0,
            take: 10,
        };
        console.log(body);
        $.post("search", JSON.stringify(body))
            .done(function (data) {
                $("#searchResult").html(data);
            })
            .fail(function (error) {
                console.error(error);
            });
    });
});
