$(document).ready(function(){
    // login / register
    translation_dict = {
        'A user with that username already exists.': 'שם המשתמש כבר קיים',
        'This password is too short. It must contain at least 8 characters.': 'הסיסמא צריכה להכיל לפחות 8 תווים',
        'This password is too common.': 'הסיסמא נפוצה מדי',
        'This password is entirely numeric.': 'הסיסמא לא יכולה להיות מורכבת רק מספרות',
        'The two password fields didn’t match.': 'הסיסמאות לא מתאימות',
        'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.': 'שם המשתמש לא תקין. שם משתמש תקין מכיל אותיות, מספרים ואת התווים הבאים: @.+-_',
        'The password is too similar to the username.': 'הסיסמא דומה מדי לשם המשתמש'
    }
    var new_errors = []
    $("ul.errorlist>li>ul.errorlist>li").each(function(){
        console.log($(this).text())
        new_errors.push(translation_dict[$(this).text()])
    });
    new_errors.forEach((item) => $("#registerErrors").append("<li>" + item +"</li>"));

    // send to relevant page
    $("button.exercise").on("click", function(){
        if ($(this).data('new')){
            window.location.href = '/אימון חדש/' + $(this).data('sendto').replaceAll('_', ' ') + '/'
        }
        else{
            window.location.href = '/' + $(this).data('sendto').replaceAll('_', ' ') + '/'
        }
    });

    // active class on collapsers
    $("#sidebarCollapse").on('click', function(){
        $("#sidebar").toggleClass('active');
    });
    $("li.active button").on('click', function(){
        console.log($(this).parent());
        $(this).parent().toggleClass('active');
    });


    // Adding options
    $("#add-options").on('dblclick', function(){
        console.log("clicked add");
    });

    // submit new exercise
    $("#exercise-template").on("submit", function(){
        $.ajax({
            method: "POST",
            url: '/create_exercise',
            data: {
                title: $("#template-title").html(),
                youtube_code: $("#txt-youtube-code").val(),
                exercises: $("#txt-excercises").val(),
                remarks: $("#txt-remarks").val()
            }, 
            success: function(response){
                alert(response);
            }
        })
    });

    // toggle fav icon
    $("#toggle_fav").on("click", function(){
        $.ajax({
            method: 'POST',
            url: '/fav',
            data: {
                title: $("#exercise-title").text().trim()
            }, 
            success: function(){
                // title star color change
                $("#toggle_fav").find('svg').toggleClass('text-secondary');
                $("#toggle_fav").find('svg').toggleClass('text-warning');

                // star show / hide from menu
                $("button.exercise[data-sendto='" + $("#exercise-title").text().trim() + "']").find('svg').toggleClass("d-none")
            }
        })
    });

    // zero modal content on modal close
    $(".modal button.btn-close").on("click", function(){
        $(this).parent().parent().find("form").find("input[type='text'], input[type='password'], input[type='email']").val("");
    })

    $("a[data-del]").on("click", function(e){
        e.stopPropagation();
        menuOptionId = $(this).data('del');
        $(this).parent().remove()
        $.ajax({
            method: 'POST',
            url: '/discard_page',
            data: {
                id: menuOptionId
            },
            success: function(response){
                console.log(response)
            }
        })
    });

    
    
});