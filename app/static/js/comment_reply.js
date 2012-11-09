(function ($) {

    var $reply_button = $('button.reply'),
        $edit_button = $('button.edit'),
        reply_form = '<form><textarea rows="1" cols="1" name="comment_text" style="display: block; margin-left: 4%; margin-top: 10px;"></textarea><button class="btn btn-mini save" type="button" style="margin-left: 4%; margin-right: 1%;">Save</button><button class="btn btn-mini cancel" type="button">Cancel</button></form>';

    $reply_button.on('click', function( event ) {
        var $container = $(this).parent()
                                .append(reply_form)
                                .find('button.save')
                                .addClass('disabled')
                                .end(),
            $comment_text = $container.find('form textarea'),
            $save_button = $comment_text.next(),
            $cancel_button = $save_button.next();

        $comment_text.on('keyup blur', function ( event ) {
            var $self = $(this);
            ( $self.val() ) ? $self.next().removeClass('disabled') :$self.next().addClass('disabled');

        });

        $cancel_button.on('click', function ( event ) {
            $(this).parent().remove();
        });

        $save_button.on('click', function ( event ) {
            event.preventDefault();

            var $self = $(this),
                comment_id = $self.parent().siblings('div.c_votes').find('a i').eq(0).data('id'),
                post_id = $('div.link div.votes').find('a i').data('id'),
                url = $SCRIPT_ROOT + '/post/' + post_id + '/' + comment_id+ '/reply';

            $.post(url, { comment: $comment_text.val() } );
            
        });


    });

    $edit_button.on('click', function ( event ) {
        var $self = $(this),
            $container = $self.parent(),
            $comment_body = $container.find('p.c_body'),
            comment_text = $.trim( $comment_body.text() );

        $comment_body.detach();
        $container.find('span.comment_info').after(reply_form);

        var $edit_form = $container.find('form textarea').first();
        $edit_form.val( comment_text );

        var $cancel_button = $container.find('button.cancel');
        $cancel_button.on('click', function ( event ) {
            $self = $(this);

            $self.parent()
                 .prev()
                 .after($comment_body)
                 .end()
                 .remove();
        });

        var $save_button = $container.find('button.save');
        $save_button.on('click', function ( event ) { 
            event.preventDefault();

            var $self = $(this),
                new_comment = $edit_form.val(),
                comment_id = $self.parent().siblings('div.c_votes').find('a i').eq(0).data('id');

            $.post( $SCRIPT_ROOT + '/comment/' + comment_id + '/edit', { new_comment: new_comment })
             .done( function ( data ) {
                 $self.parent()
                      .prev()
                      .after($comment_body.text(new_comment).hide().fadeIn('slow'))
                      .end()
                      .remove();
             });
        });

    });


})(jQuery);
