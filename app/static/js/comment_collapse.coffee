(($) ->
  toggle_button = "<span class='collapse_handle' style='cursor:pointer;margin-left:23px;margin-right:-26px;font-weight:bold;'>[-]</span>"
  $comments = $('div.comment')

  $comments.find('.comment_info').before(toggle_button)

  expandOrCollapse = (direction) ->
    self = this
    parent_offset = self.parent().css('margin-left')

    #loop through each child comment, hide/show if offset is greater
    for comment in self.parent().nextAll()
      current_offset = $(comment).css('margin-left')

      if current_offset > parent_offset
        if direction is 'up' then $(comment).slideUp('fast') else $(comment).slideDown('fast')
      else
        return false

  hideChildren = ->
    $self = $(this)

    expandOrCollapse.call $self, 'up'

    $self.text('[+]').addClass('expand_handle').removeClass('collapse_handle')
    #hide comment body and reply/edit buttons
    $self.parent().css('margin-bottom',0).find('.comment_info').nextAll().hide()
    #hide voting arrows
    $self.prev().hide()

    $self.off('click').on('click', showChildren)

  showChildren = ->
    $self = $(this)

    expandOrCollapse.call $self, 'down'

    $self.text('[-]').addClass('collapse_handle').removeClass('expand_handle')
    #show comment body and buttons, reset margin
    $self.parent().css('margin-bottom',10).find('.comment_info').nextAll().show()
    #show votes
    $self.prev().show()

    $self.off('click').on('click', hideChildren)

  $('span.collapse_handle').on 'click', hideChildren

)(jQuery)
