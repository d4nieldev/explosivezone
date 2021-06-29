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
        window.location.href = '/' + $(this).data('sendto') + '/'
    });

    // active class on collapsers
    $("#sidebarCollapse").on('click', function(){
        $("#sidebar").toggleClass('active');
    });


    // Adding options
    $(document).on('dblclick', 'a.add-option', function(){
        $(this).parent().html("<input id='txt-add-option' type='text' class='bg-transparent form-control text-white' style='font-size: 1.1rem' />");
        $("#txt-add-option").trigger('focus');
    });
    $(document).on('blur', '#txt-add-option', function(){
        $(this).parent().html("<a class='add-option'>הוספה</a>");
    });
    $(document).on('keypress', '#txt-add-option', function(e){
        if (e.which == 13 && $(this).val().length > 0){
            element = $(this)
            $.ajax({
                method: 'POST',
                url: '/create_menu_option',
                data: {
                    parent_title: $(element).parent('li').parent('ul').parent('li').children('button').text(),
                    title: $(element).val()
                },
                success: function(response){
                    alert(response);
                }

            })
        }
    });
    
    $("#sidebar>.components button").on('click', function(){
        current_level = $(this).parent().parents().length
        original_element = $(this);

        $("li.active").each(function(){
            if ($(this).parents().length >= current_level && $(this).children('button')[0] != original_element[0]){
                // link already opened in the same level
                collapseOption($(this));
            }
        });
        $(this).parent().toggleClass("active");
    });

    $("#exercise-template").on("submit", function(){
        $.ajax({
            method: "POST",
            url: '/create_exercise',
            data: {
                title: $("#template-title").html(),
                youtube_code: $("#txt-youtube-code").val(),
                exercises: $("#txt-excercises").val(),
                remarks: $("#txt-remarks").val()
            }, success: function(response){
                alert(response);
            }
        })
    });
    
});