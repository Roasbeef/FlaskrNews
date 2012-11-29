//TODO:
//    Attatch Votes after new posts load in
(function ( $ ) {
    
    var navLinks = $('.nav:eq(0) > li').not('.divider-vertical').slice(0,2);

    function scrollLoad () {
        var wantsHot = $(navLinks[0]).hasClass('active'),
            $cur_info = $('#cur_info').detach(),
            cur_string = $cur_info.data('cur_string'),
            page_num = parseInt($cur_info.data('page_num')) + 1,
            more = $cur_info.data('more_content'),
            $new_posts = $('<div>'),
            speed = 2000,
            url = '/';

            if (!more) return false;

            return $new_posts.load(url + ' .link_wrapper > ', { cur_string: cur_string, page_num: page_num, sort: (wantsHot) ? 'hot' : 'new' },
            function () {
                console.log($new_posts);
                $new_posts.children()
                          .hide()
                          .appendTo('.link_wrapper')
                          .fadeIn(speed);
                console.log($cur_info);
            });

    }

    var past_point = false;

    $(window).on('scroll', function () {
        var $self = $(this),
            doc_height = $(document).height(),
            scroll_pos = $self.scrollTop(),
            load_point = doc_height / 4;


        if ( !past_point ) {

            if ( scroll_pos > load_point ) {
                past_point = true;
                console.log('try');
                $.when( scrollLoad() ).then( function () {
                    past_point = false;
                    console.log('good loop');
                });
            }
        }

    });

})(jQuery)
