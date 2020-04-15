$(document).ready(function(){
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

    
    $("#cart").on("click", ".del", function () {  //$(".del").click(function() //---> //because event handlers will be lost when the elements are replaced //$("#parent").on("click", ".item-to-be-clicked", function () {
        $.post('/del_cart_item/', { cartitemid: $(this).attr("idincart")} , function(data){
            //$("#notif").html(data);
            $("#cart").html($(data).find("#cart")); //replace new part of cart with old part
            $("#cart_total").html($(data).find("#cart_total")); //replace new total price with old

        }).done(function () {
            $('.alert').addClass('alert-success').addClass("show").html("<strong>DELETED</strong>");
            $(".alert").delay(2000).addClass("in").toggle(true).fadeOut(1000);
        }).fail(function () {
            $('.alert').addClass('alert-danger').addClass("show").html("<strong>ERROR IN DELETE THIS ITEM</strong>");
            $(".alert").delay(2000).addClass("in").toggle(true).fadeOut(1000);
        })
    });

    $("#cart").on("change", ".quantity", function () {  
        //complicate select for new_order_num !!!!!!!!!!!!!
        $.post('/calcu_cart_item/', { cartitemid: $(this).attr("idincart"), new_order_num: $('input[idincart=' + $(this).attr("idincart") + ']').val() }, function (data) { 
            $("#cart").html($(data).find("#cart"));  
            $("#cart_total").html($(data).find("#cart_total"));
            
        }).done(function () {
            //do smt
        }).fail(function () {
            $('.alert').addClass('alert-danger').addClass("show").html("<strong>ERROR IN UPDATE THIS ITEM</strong>");
            $(".alert").delay(2000).addClass("in").toggle(true).fadeOut(1000);
        })
    });

    if($(".outnumber").text().length){
        $("#checkout").addClass("disabled");
    }
    else {
        $("#checkout").addClass("active");
    }

});