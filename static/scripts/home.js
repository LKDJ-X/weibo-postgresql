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

function addPost(user_name, date, content, id, likes, reverse) {
    var html = '\
    <div class="media" id ="' + id + '">\
        <div class="media-left">\
            <a href="#">\
                <img class="media-object" data-src="holder.js/64x64" alt="64x64" src="/static/img/user.png" data-holder-rendered="true">\
            </a>\
        </div>\
        <div class="media-body">\
            <h4 class="media-heading">' + user_name + ' <small class="date">' + date + '</small></h4>\
            <div id="' + id + '" class="content">' + content + '</div>\
            <button id="' + id + '" type="button" name="edit_post" class="btn btn-default delete">\
                <span id="' + id + '" class="glyphicon glyphicon-edit" aria-hidden="true"></span>\
            </button>\
            <button id="' + id + '" type="button" name="like_post" class="btn btn-default like"' + (likes > 0 ? 'style="color:#FF3333;"' : '') + '>\
                <span id="' + id + '" class="glyphicon glyphicon-heart-empty" aria-hidden="true"> ' + likes + '</span>\
            </button>\
            <button id="' + id + '" type="button" name="delete_post" class="btn btn-default delete" onclick="delete_post(' + id + ')">\
                <span id="' + id + '" class="glyphicon glyphicon-remove-circle" aria-hidden="true"></span>\
            </button>\
        </div>\
        <div id="' + id + '" class="edit_field" style="display: none;" name="edit_field">\
                <textarea id="' + id + '" name="edit_post" type="content" placeholder="Edit post">' + content + '</textarea><br>\
                <button id="' + id + '" type="button" name="submit_edit_post" class="btn btn-default btn-xs">\
                    <span id="' + id + '" class="glyphicon glyphicon-check" aria-hidden="true"></span>\
                </button>\
        </div>\
    </div>';

    var div = document.createElement('div');
    div.className = 'post';
    div.id = id;
    div.innerHTML = html;

    console.log($(div));

    if (reverse) {
        $('#container').prepend(div)
    } else {
        $('#container').append(div)
    }

    $('button[name="like_post"][id=' + id + ']').click(function (e) {
        var target = $(e).attr('target');
        var button = this;
        var spanc = $("span#" + id).class;
        if (span == "glyphicon glyphicon-heart-empty") {
            $.post('like_post/' + id, function (data) {
                var json = JSON && JSON.parse(data) || $.parseJSON(data);
                if (json.success) {
                    button.style.color = "#ff3333";
                    var like = $("span#" + id + ".glyphicon-heart");
                    var likeint = parseInt(like.text());
                    like.text(' ' + (likeint + 1));
                    $("span#" + id).class = "glyphicon glyphicon-heart";
                } else {
                    // TODO Print error
                }
            });

        } else {
            $.post('dislike_post/' + id, function (data) {
                var json = JSON && JSON.parse(data) || $.parseJSON(data);
                if (json.success) {
                    button.style.color = "";
                    var like = $("span#" + id + ".glyphicon-heart");
                    var likeint = parseInt(like.text());
                    like.text(' ' + (likeint - 1));
                    $("span#" + id).class = "glyphicon glyphicon-heart-empty";
                } else {
                    // TODO Print error
                }
            });
        }

    });
}