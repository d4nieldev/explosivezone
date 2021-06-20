$(document).ready(function(){
    if ($("#is_admin").html() == "True"){
        $("a.add-page").removeClass('d-none');
    }
    else{
        $("a.add-page").addClass('d-none');
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
            }
        })
    });

    $(".sidebar-header>h3").on("click", function(){
        $("#exercise-container").addClass('d-none');
        $("#homepage-container").removeClass('d-none');
    });

    $("#sidebarCollapse").on('click', function(){
        $("#sidebar").toggleClass('active');
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
});