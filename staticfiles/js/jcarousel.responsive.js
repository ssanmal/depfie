(function($) {
    $(function() {
        var jcarousel = $('.jcarousel');

        jcarousel
            .on('jcarousel:reload jcarousel:create', function () {
                var carousel = $(this),
                    width = carousel.innerWidth();

                width = width / 1.4;

                carousel.jcarousel('items').css('width', Math.ceil(width) + 'px');
            })
            .jcarousel({
                wrap: 'circular'
            })
            .jcarouselAutoscroll({
            interval: 3000,
            target: '+=2',
            autostart: true
            });

        $('.jcarousel-control-prev')
            .jcarouselControl({
                target: '-=2'
            });

        $('.jcarousel-control-next')
            .jcarouselControl({
                target: '+=2'
            });

        $('.jcarousel-pagination')
            .on('jcarouselpagination:active', 'a', function() {
                $(this).addClass('active');
            })
            .on('jcarouselpagination:inactive', 'a', function() {
                $(this).removeClass('active');
            })
            .on('click', function(e) {
                e.preventDefault();
            })
            .jcarouselPagination({
                perPage: 2,
                item: function(page) {
                    return '<a href="#' + page + '">' + page + '</a>';
                }
            });

    });
})(jQuery);