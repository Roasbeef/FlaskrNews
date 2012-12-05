(($) ->
  $reply_button = $('button.reply')
  $edit_button  = $('button.edit')
  reply_form    = '<form id="change"><textarea rows="1" cols="1" name="comment_text" style="display: block; margin-left: 4%; margin-top: 10px;"></textarea><button class="btn btn-mini save" type="button" style="margin-left: 4%; margin-right: 1%;">Save</button><button class="btn btn-mini cancel" type="button">Cancel</button></form>'

  $reply_button.on 'click', (e) ->
    $container     = $(this).parent()
    #don't add more than one form
    unless $container.find('form#change').length
      $container.append(reply_form).find('button.save').addClass('disabled')

    $comment_text  = $container.find('form textarea')
    $save_button   = $comment_text.next()
    $cancel_button = $save_button.next()

    #disable submit if comment is blank
    $comment_text.on 'keyup blur', (e) ->
      console.log 'k'
      $self = $(this)
      if $self.val() then $self.next().removeClass('disabled') else $self.next().addClass('disabled')

    #remove input box on click
    $cancel_button.on 'click', (e) ->
      console.log 'k'
      $(this).parent().remove()

    $save_button.on 'click', (e) ->
      e.preventDefault()

      $self      = $(this)
      comment_id = $self.parent().siblings('div.c_votes').find('a i').eq(0).data('id')
      post_id    = $('div.link div.votes').find('a i').data('id')
      reply_url  = "/post/#{post_id}/#{comment_id}/reply"

      #send comment reply off to the server
      $.post(reply_url, comment: $comment_text.val())
       .done ->
         #get most recent comment to display
         $.get "/comment/_newest", post: post_id, author: "x", (data) ->
           $new_comment    = $(data)
           container_width = $('.link_wrapper').width()
           #calculate percentage offset
           parent_width    = Math.ceil( ( parseInt( $container.css('margin-left') ) / container_width ) * 100 )
           $self.closest('form#change').remove()
           $new_comment.hide().css('margin-left', "#{parent_width + 3}%").insertAfter($container).fadeIn('slow')


  $edit_button.on 'click', (e) ->
    $self         = $(this)
    $container    = $self.parent()
    $comment_body = $container.find('p.c_body')
    comment_text  = $.trim $comment_body.text()

    #detach original comment and attach edit form
    unless $container.find('form#change').length
      $comment_body.detach()
      $container.find('span.comment_info').after(reply_form)

    $edit_form     = $container.find('form textarea').first()
    $cancel_button = $container.find('button.cancel')
    $save_button   = $container.find('button.save')

    $edit_form.val comment_text if comment_text

    $cancel_button.on 'click', (e) ->
      $self = $(this)
      $self.parent().prev().after($comment_body).end().remove()
    
    $save_button.on 'click', (e) ->
      e.preventDefault()
      
      $self       = $(this)
      new_comment = $edit_form.val()
      comment_id  = $self.parent().siblings('div.c_votes').find('a i').eq(0).data('id')

      $.post("/comment/#{comment_id}/edit", new_comment: new_comment)
       .done (data) ->
         $self.parent().prev().after($comment_body.text(new_comment).hide().fadeIn('slow'))
              .end().remove()
              
)(jQuery)
