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
    $(".pg").click(function () {
       //alert($(this).text()); 
    
        $.get('/catalog/', { pgnum: $(this).text() }, function (data) {
            //$("#notif").html(data);
            $("#pros").html($(data).find("#pros")); //replace new part of cart with old part

        }).done(function () {
            alert("DONE");
        });
    
    });

    
    $("select").change(function(){ //for when sizepicker or genderpicker change
        filter();
    });

    $(".category-check-boxes").change(function () { //for when category checkboxes change
        filter();    
    });
    
    function filter(){
        size = $("#sizepicker").val();
        gender = $("#genderpicker").val() ;
        var checkboxValues = [];
        $('input[type="checkbox"]:checked').each(function (index, elem) {
            checkboxValues.push($(elem).val());
        });
        category = checkboxValues.join(', '); //for change array to str
        size = size.join(', '); //for change array to str
        sortby = $('.sortpros a').attr("sortby");
        
        //alert(size+" "+gender+" "+category+" .");
        
        $.get('/catalog/', { size: size, gender: gender, category: category, sortby: sortby }, function (data) {
            //$("#notif").html(data);
            $("#pros").html($(data).find("#pros")); //replace new part of cart with old part

        }).done(function () {
            //alert("DONE");
            //$(".primary-color").text("DONE")
            $('.alert').addClass('alert-success').addClass("show").html("<strong>Filter is Success</strong>");
            $(".alert").delay(2000).addClass("in").toggle(true).fadeOut(1000);
        
        }).fail(function () {
            //alert("FAIL");
            $('.alert').addClass('alert-danger').addClass("show").html("<strong>ERROR in Filtering</strong>");
            $(".alert").delay(2000).addClass("in").toggle(true).fadeOut(1000);
        });     
    }

    //for dropdown items text changing when selected
    $('.dropdown-menu').on('click', 'a', function () {
        var text = $(this).html();
        var htmlText = text + ' <span class="caret"></span>';
        $(this).closest('.dropdown').find('.dropdown-toggle').html(htmlText);
    }); 

    // for Sort items in catalog page
    $('.sortpros').on('click', 'a', function () {
        //alert ( $(this).attr("sortby") );

        $.get('/catalog/', { sortby: $(this).attr("sortby") }, function (data) {
            $("#pros").html($(data).find("#pros")); //replace new part of cart with old part

        }).done(function () {
            alert("DONE");
        }).fail(function () {
           alert("FAIL"); 
        });

    });


});