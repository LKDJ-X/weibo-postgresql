//show more editing area when click the textarea
$("#content").click(function (e) {
    $("#post-area").addClass("higher");
    e.stopPropagation();
});

//close the extented textarea
$("body").click(function (e) {
    if(e.target.id !== "post_btn"){
        $("#post-area").removeClass("higher");
    }
});

