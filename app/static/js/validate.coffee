(($) ->
  $register  = $('a#register')
  $container = $('.form-container')

  displayMessage = (type, message) ->
    input_box = @.closest('.control-group')
    show_message = => $('.help-inline', @.parent()).text(message)

    if type is 'success'
      input_box.removeClass('error').addClass('success')
      show_message()
      #allow submition
      $('button').removeClass('disabled').closest('form').off()
    else
      input_box.removeClass('success').addClass('error')
      show_message()
      #show disabled and prevent submition
      $('button').addClass('disabled').closest('form')
                 .on 'click', (e) ->
                   return false

  $register.on 'click', (e) ->
    e.preventDefault()
 
    $.get('/register', (result) ->
      $container.html(result))
     .then ->
       $user_input = $('input#inputUsername')
       $confirm = $('input#inputConfirm')
 
       #attach message span to form
       $('<span class="help-inline"></span>').appendTo('.controls')
 
       $user_input.on 'blur', ->
 
         #was the username left blank?
         if not $.trim($(@).val())
           displayMessage.call $(@), 'error', 'Username required!'
           return
 
         $.getJSON '/_check_username', username: $user_input.val(),
           (data) =>
             if data.result is "all good"
               displayMessage.call $(@), 'success', 'Username is available!'
             else
               displayMessage.call $(@), 'error', 'Username is taken!'
 
       $confirm.on 'blur', ->
         $pass = $('input#inputPassword')
 
         if $(@).val() isnt $pass.val()
           displayMessage.call $(@), 'error', 'Passwords must match!'
           displayMessage.call $pass, 'error', ''
         else
           displayMessage.call $(@), 'success', ''
           displayMessage.call $pass, 'success', ''
)(jQuery)
