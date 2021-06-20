$(document).ready(function(){
    $("#sidebar ul").append("<li><a class='add-option d-none'>הוספה</a></li>");
    
    if ($("#is_admin").html() == "True"){
        $("a.add-page").removeClass('d-none');
        $("a.add-option").removeClass('d-none');
    }
    else{
        $("a.add-page").addClass('d-none');
        $("a.add-option").addClass('d-none');
    }

    $("button.exercise").on("click", function(){
        $.ajax({
            url: '/show_exercise',
            method: 'POST',
            data: {
                exercise_title: $(this).data('sendto'),
            },
            success: function(data){
                $("#exercise-title").html(data.title);

                $("#exercise-video").html('<iframe src="' + data.youtube_link + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');

                exercises_html = "";
                data.exercise_list.forEach(exercise => {
                    exercises_html += "<li>" + exercise + "</li>"
                });
                $("#exercise-content>ul").html(exercises_html);

                $("#exercise-remarks").html(data.remarks);
                $("#exercise-container").removeClass('d-none');
                $("#homepage-container").addClass('d-none');
                $("#exercise-template-container").addClass('d-none');
            }
        })
    });

    $(".sidebar-header>h3").on("click", function(){
        $("#homepage-container").removeClass('d-none');
        $("#exercise-container").addClass('d-none');
        $("#exercise-template-container").addClass('d-none');
    });

    $("a.add-page").on("click", function(){
        $("#template-title").html($(this).parent('button').text());

        $("#exercise-template-container").removeClass('d-none');
        $("#homepage-container").addClass('d-none');
        $("#exercise-container").addClass('d-none');
    });

    $("#sidebarCollapse").on('click', function(){
        $("#sidebar").toggleClass('active');
    });

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
        console.log("current_level: " + current_level);
        $("li.active").each(function(){
            console.log(original_element[0])
            console.log($(this).children('button')[0])
            if ($(this).parents().length >= current_level && $(this).children('button')[0] != original_element[0]){
                // link already opened in the same level
                $(this).removeClass('active');
                if ($(this).children('button').hasClass('dropdown-toggle')){
                    $(this).children('button').attr('aria-expanded', 'false');
                    $(this).children('button').addClass('collapsed');
                    $(this).children('ul').removeClass('show');
                }
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