function set_active(current_page_title) {
    /**
     * make red background for selected items on page load
     */

    $(".components li>button.exercise").each(function () {
        if ($(this).text().trim() === current_page_title) {
            $(this).parentsUntil('ul.components').each(function () {
                $(this).addClass('active');
                if ($(this).find('button').hasClass('dropdown-toggle')) {
                    $(this).find('button').attr("aria-expanded", 'true');
                    $(this).find('button').removeClass('collapsed');
                    $(this).find('ul').addClass('show');
                }
            });
        }
    });
}

$(document).ready(function () {
    set_active($("#exercise-title").text().trim());
    // page navigation
    $("button.exercise").on("click", function () {
        if ($(this).data('new')) {
            window.location.href = '/אימון חדש/' + $(this).data('sendto').replaceAll('_', ' ') + '/'
        } else {
            window.location.href = '/אימון/' + $(this).data('sendto').replaceAll('_', ' ') + '/'
        }
    });

    const translation_dict = {
        'A user with that username already exists.': 'שם המשתמש כבר קיים',
        'This password is too short. It must contain at least 8 characters.': 'הסיסמא צריכה להכיל לפחות 8 תווים',
        'This password is too common.': 'הסיסמא נפוצה מדי',
        'This password is entirely numeric.': 'הסיסמא לא יכולה להיות מורכבת רק מספרות',
        'The two password fields didn’t match.': 'הסיסמאות לא מתאימות',
        'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.': 'שם המשתמש לא תקין. שם משתמש תקין מכיל אותיות, מספרים ואת התווים הבאים: @.+-_',
        'The password is too similar to the username.': 'הסיסמא דומה מדי לשם המשתמש',
        'The password is too similar to the email address.': 'הסיסמא דומה מדי לאימייל'
    }

    // store and translate errors from login or register modals
    let new_errors = [];
    $("ul.errorlist>li>ul.errorlist>li").each(function () {
        console.log($(this).text())
        new_errors.push(translation_dict[$(this).text()])
    });
    // view the errors in the right place
    new_errors.forEach((item) => $("#registerErrors").append("<li>" + item + "</li>"));

    // open and close sidebar
    $("#sidebarCollapse").on('click', function () {
        $("#sidebar").toggleClass('active');
    });

    // toggle active class on buttons 
    $(".components li button").on("click", function () {
        $(this).parent().toggleClass("active");
    });

    // submit new exercise
    $("#exercise-template").on("submit", function () {
        $.ajax({
            method: "POST",
            url: '/create_exercise',
            data: {
                title: $("#template-title").html(),
                youtube_code: $("#txt-youtube-code").val(),
                exercises: $("#txt-excercises").val(),
                remarks: $("#txt-remarks").val()
            },
            success: function (response) {
                console.log(response);
            }
        })
    });

    // zero modal content on modal close
    $(".modal button.btn-close").on("click", function () {
        $(this).parent().parent().find("form").find("input[type='text'], input[type='password'], input[type='email']").val("");
    })

    // delete menu options
    $("a[data-del]").on("click", function (e) {
        e.stopPropagation();
        menuOptionId = $(this).data('del');
        $(this).parent().remove()
        $.ajax({
            method: 'POST',
            url: '/discard_page',
            data: {
                id: menuOptionId
            },
            success: function (response) {
                console.log(response)
            }
        })
    });
});