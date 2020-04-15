$(document).ready(function () {
    ////////////////////////////* becuse CSRF get error on ajax post  *//////////////////////////////////
    // This will allow to get csrf token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // This will send csrf token on every ajax request
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    ////////////////////////////* becuse CSRF get error on ajax post  *//////////////////////////////////

    //for product images
    $(".mainimage").attr('src',$('.subimage').attr('src')); 
    $(".subimage").click(function(){    
        $(".mainimage").attr('src', $(this).attr('src'));
    });

    $("#myselect").change(function () { //for select color and sizes
        $("#addtocart").removeAttr('disabled');
    });

    ////////////////////////////////////* For Load More Comment *////////////////////////////////////////////////
    $("#loadmorebtn").click(function () {  
        //$(".del").click(function() //---> //because event handlers will be lost when the elements are replaced //$("#parent").on("click", ".item-to-be-clicked", function () {    
        var url = "/detail/"+$(this).attr("pk")+"/";
        $.post( url , { loadmorecomment: $("#loadmorebtn").attr('count') }, function (data) {
            //$("#notif").html(data);
            $("#commentsection").html($(data).find("#commentsection")); //replace new part of cart with old part

        }).done(function () {
            //alert("ok");
            var count = parseInt($("#loadmorebtn").attr('count')) + 1;
            $("#loadmorebtn").attr('count', count.toString());
        }).fail(function () {
            alert("Fail");
        });
    });
    ////////////////////////////////////* For Delete Comment *////////////////////////////////////////////////
    $("#commentsection").on("click", ".del-comment", function () {
        var url = "/detail/" + $("#loadmorebtn").attr("pk") + "/";
        $.post(url, { pk: $(this).attr("pk") , deletecomment:'deletecomment' }, function (data) {
            $("#commentsection").html($(data).find("#commentsection"));
        }).done(function () {
            alert("Delete Comment Successfully");
        }).fail(function () {
            alert("Error in Delete This Comment");
        });
    });
    ////////////////////////////////////* For Like Comment *////////////////////////////////////////////////
    $("#commentsection").on("click", ".like", function () {
        var pk = $(this).attr("pk") ;
        $.post('/like_dislike/', { pk: pk , like:"like" }, function (data) {
            //replace new like number and dislike number
            $("span[liked-pk=" + pk + "]").text(data.liked);
            $("span[disliked-pk=" + pk + "]").text(data.disliked);

        }).done(function () {
            //set like button green and dislike button white
            $(".like[pk=" + pk + "]").addClass("thumbs-green");
            $(".dislike[pk=" + pk + "]").removeClass("thumbs-red");
        }).fail(function () {
            alert("Fail");
        });

    });
    ////////////////////////////////////* For Dislike Comment *////////////////////////////////////////////////
    $("#commentsection").on("click", ".dislike", function () {
        var pk = $(this).attr("pk");
        $.post('/like_dislike/', { pk: pk, dislike: "dislike" }, function (data) {
            //replace new like number and dislike number
            $("span[disliked-pk=" + pk + "]").text(data.disliked);
            $("span[liked-pk=" + pk + "]").text(data.liked);

        }).done(function () {
            //set dislike button red and like button white
            $(".dislike[pk=" + pk + "]").addClass("thumbs-red");
            $(".like[pk=" + pk + "]").removeClass("thumbs-green");;
        }).fail(function () {
            alert("Fail");
        });   
    });



    $(".like").hover(function() {
        $(this).toggleClass("btn-primary");
    });
    $(".dislike").hover(function () {
        $(this).toggleClass("btn-primary");    
    });

});