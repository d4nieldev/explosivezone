$(document).ready(function(){
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
});