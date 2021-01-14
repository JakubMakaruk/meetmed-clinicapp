document.addEventListener('DOMContentLoaded', function() {
    $(document).ready(function() {
        $.each($('#navbar').find('li'), function() {
            $(this).toggleClass('active', 
                window.location.pathname.indexOf($(this).find('a').attr('href')) > -1);
        }); 
    });

    $('.news-carousel').slick({
        autoplay: false,
        autoplaySpeed: 3500,
        mobileFirst: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 1,
                }
            },
            {
                breakpoint: 1600,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
});