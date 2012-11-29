$(function () {
    var register = $('a#register'),
        container = $('.form-container'),
        user_input;

    function displayMessage(type, message) {
        var $self = $(this),
            input_box = $self.closest('.control-group'),
            show_message = function () {
                $('.help-inline', $self.parent() ).text( message );
            };


        if ( type == 'success' ) {
            input_box.removeClass('error').addClass('success');
            show_message();
            $('button').removeClass('disabled').closest('form').off();

        } else {
            input_box.removeClass('success').addClass('error');
            show_message();
            $('button').addClass('disabled').closest('form').on('submit', function ( e ) {
                return false;
            });
        }
    }

    register.on('click', function ( e ) {
        e.preventDefault();

        $.get('/register', function ( result ) {
            container.html(result);
        }).then( function () {
                var user_input = $('input#inputUsername'),
                confirm = $('input#inputConfirm');
            
            $('<span class="help-inline"></span>').appendTo('.controls');

            user_input.on('blur', function () {
                $self = $(this);

                $.getJSON( $SCRIPT_ROOT + '/_check_username', {
                    username: user_input.val()
                }, function ( data ) {
                    if ( data.result  == "all good"  && $.trim($self.val() ) ) {
                        displayMessage.call( $self, 'success', 'Username is available!');
                    } else if ( !$.trim($self.val() ) ) {
                        displayMessage.call( $self, 'error', 'Username required!');
                    } else {
                        displayMessage.call( $self, 'error', 'Username is taken!');
                    }
                });
            });

            var $pass = $('input#inputPassword');

            confirm.on('blur', function () {
                var $self = $(this);
                
                if ( $self.val() != $pass.val() ) {
                    displayMessage.call( $self, 'error', 'Passwords must match!');
                    displayMessage.call( $pass, 'error', '');

                } else {
                    displayMessage.call( $self, 'success', '');
                    displayMessage.call( $pass, 'success', '');
                }
            });

        });

    });
})
