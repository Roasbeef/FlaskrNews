(function( $ ){

    var navLinks = $('.nav:eq(0) > li').not('.divider-vertical').slice(0,2),
        container = $('.link_wrapper');

    function isLoggedIn() {
        return $('.nav.pull-right li.dropdown').length;
    }

    navLinks.on('click', function ( e ) {
        $self = $(this);

        $self.siblings()
             .not('.divider-vertical')
             .removeClass('active');

        $self.addClass('active');

        e.preventDefault();

    });
    
    navLinks.slice(0,2).on('click', function ( e ) {
        var url = ( $(this).text().toLowerCase() === 'new' ) ? '/?sort=new' : '/';

        $("html, body").animate({ scrollTop: 0 }, 600);
        
        container.fadeOut('slow', function () {
            $.when( container.load(url + ' .link_wrapper > ') ).then( function () {
                container.fadeIn('slow', function () {
                    if (isLoggedIn()) attachVotes();
                });
            });
        });
    });

    function attachVotes() {

        $('[class^="icon-chevron"]').each( function( index, e ) {
            $(e).on('click', function ( event ) {
                event.preventDefault();

                var $self = $(this),
                    direction = ( $self.hasClass('up') ) ? 1 : -1;

                vote.call( $self, direction, $self.data('id') );

            });
        });

    }


    function vote( direc, id ) {
            var $self = $(this);

            $self.fadeOut('fast')
                 .parent().siblings().find('i').fadeIn('fast');

            $.post( $SCRIPT_ROOT + '/post/_vote/' + id, { direction: direc }).done( function () {
                var $score_button = $self.closest('.link').find('button'),
                    score        = parseInt($score_button.text());

                $score_button.text( (score + direc) + ' Points');

            });
    }

    if (isLoggedIn()) attachVotes();

})(jQuery)
