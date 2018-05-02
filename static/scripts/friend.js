//
var $ul = $("#nav_list");
var $lis = $("li", $ul);
var $tabs = $(".tab");

var $search = $("#search_tab");
var $follower = $("#followers_tab");
var $following = $("#following_tab");

var $searchBar = $("#search");

var MYAPP = {
    "liClass": "selected",
    "tabClass": "current",
    "url": {
        "follower_list": "/follower_list",
        "following_list": "/following_list",
        "search": "/search_user"
    }
}

//main frame
$ul.on("click", "li",function () {
    $lis.removeClass(MYAPP.liClass);
    $tabs.removeClass(MYAPP.tabClass);

    $(this).addClass(MYAPP.liClass);

    switch(this.id){
        case "search_li":
            $search.addClass(MYAPP.tabClass);
            //changeStatus($(".results", $search)[0], "init");
            break;
        case "follower_li":
            $follower.addClass(MYAPP.tabClass);
            follwers();
            break;
        case "following_li":
            $following.addClass(MYAPP.tabClass);
            following();
            break;
    }
});

function follwers() {
    var $items = $(".items", $follower);
    var resultsDom = $(".results", $follower)[0];
    changeStatus(resultsDom, "searching");

    $.getJSON(MYAPP.url.follower_list, function (res) {
        var template = _.template($('#template').html());
        var arr = [];
        var results = res.results;

        if(res.success && results.length > 0){
            for(var i = 0; i < results.length; i++){
                arr.push(template(_.extend(results[i], {
                    follow: false,
                    unfollow: false
                })))
            }
            $items.html(arr.join(""))
            changeStatus(resultsDom, "full");
        }
        else{
            //...no result
            changeStatus(resultsDom, "empty");
        }
        $items.prepend("Total:" + results.length);
    });
}

function following() {
    var $items = $(".items", $following);
    var resultsDom = $(".results", $following)[0];
    changeStatus(resultsDom, "searching");

    $.getJSON(MYAPP.url.following_list, function (res) {
        var template = _.template($('#template').html());
        var arr = [];
        var results = res.results;

        if(res.success && results.length > 0){
            for(var i = 0; i < results.length; i++){
                arr.push(template(_.extend(results[i], {
                    follow: false,
                    unfollow: true
                })))
            }
            $items.html(arr.join(""))
            changeStatus(resultsDom, "full");
        }
        else{
            //...no result
            changeStatus(resultsDom, "empty");
        }
        $items.prepend("Total:" + results.length);
    });
}

//按照姓名、邮箱搜索用户
$searchBar.on("input", function () {
    console.log(this.value);
    var value = this.value.trim();
    var resultsDom = $(".results", $search)[0];
    changeStatus(resultsDom, "searching");

    if(value){
        $.getJSON(MYAPP.url.search + "/" + value, function (res) {
        var template = _.template($('#template').html());
        var arr = [];
        var results = res.results;

        if(res.success && results.length > 0){
            for(var i = 0; i < results.length; i++){
                arr.push(template(_.extend(results[i], {
                    follow: true,
                    unfollow: false
                })))
            }
            $(".items", $search).html(arr.join(""))
            changeStatus(resultsDom, "full");
        }
        else{
            //...no result
            changeStatus(resultsDom, "empty");
        }
    });
    }
    else{
        changeStatus(resultsDom, "init");
    }
});

//follow & unfollw
$(".items", $("#search_tab, #following_tab")).on("click", "a", function () {
    var type = $(this).data("type");
    $.post($(this).data("url"), function (res) {
        res = JSON.parse(res);

        if(res.success){
            if(type === "unfollow"){
                $("#following_li").click();
            }
            alert("Success");
        }
        else{
            alert(res.error);
        }
    });
})


//common functions
function changeStatus(results,className) {
    results.className = "results " + className;
}