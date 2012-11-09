(function( $ ) {
    var toggle_button = "<span class='collapse_handle' style='cursor:pointer;margin-left:23px;margin-right:-26px;font-weight:bold;'>[-]</span>",
        $comments = $('div.comment');

    //attach toggle button to each comment
    $comments.find('.comment_info').before(toggle_button);

    $('.collapse_handle').on('click', function ( event ) {
        var $self = $(this),
            parent_offset = $self.parent().css('margin-left');

        event.preventDefault();

        //loop through each child, hide if offset is greater
        $self.parent().nextAll().each( function ( i, e ) {
            var current_offset = $(this).css('margin-left');

            if ( current_offset > parent_offset ) {
                $(this).slideUp();
            } else {
                return false; 
            }

            $self.parent().css('margin-bottom',0).find('.comment_info').nextAll().hide();
            $self.text('[+]').removeClass('collapse_handle').addClass('expand_handle');
            $self.prev().hide();

        });
    });

    $('.expand_handle').on('click', function ( event ) {
        console.log('f');
        var $self = $(this),
            parent_offset = $self.parent().css('margin-left');

        event.preventDefault();

        $self.parent().nextAll().each( function ( i, e ) {
            var current_offset = $(this).css('margin-left');

            if ( current_offset > parent_offset ) {
                $(this).slideDown();
            } else {
                return false;
            }

            $self.parent().css('margin-bottom',25).find('.comment_info').nextAll().show();
            $self.text('[-]').addClass('collapse_handle').removeClass('expand_handle');
            $self.prev().show();

        });

    });


})( jQuery );
