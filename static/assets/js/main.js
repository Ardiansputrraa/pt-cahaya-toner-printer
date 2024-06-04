(function ($) {
    "use strict";

    // Spinner
    let spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1)
    }
    spinner()

    // Progress Bar
    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%')
        })
    }, {offset: '80%'})


    // Warna Grafik
    Chart.defaults.color = "#6C7293"
    Chart.defaults.borderColor = "#000000"
    
})(jQuery);

