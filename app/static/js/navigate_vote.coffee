(($) ->
  
  $navLinks = $('.nav:eq(0) > li').not('divider-vertical')[0...2]
  $links_container = $('.link_wrapper')

  isLoggedIn = -> $('.nav.pull-right li.dropdown').length

  vote = (direc, id)->
    $self = $(this)

    #hide clicked arrow show other arrow
    $self.fadeOut('fast')
         .parent().siblings().find('i').fadeIn('fast')

    $.post("/post/_vote/#{id}", direction: direc)
     .done ->
       $score_button = $self.closest('.link').find('button')
       score = parseInt( $score_button.text() )

       #update old score by new direction
       $score_button.text "#{score + direc} Points"

  attachVotes = ->
    for arrow in $('[class^="icon-chevron"]')
      $(arrow).on 'click', (e) ->
        e.preventDefault()

        $self = $(this)
        direction = if $self.hasClass('up') then 1 else -1

        vote.call $self, direction, $self.data('id')

  # Toggle "active" class when nav links are clicked
  $navLinks.on 'click', (e) ->
    e.preventDefault()

    $self = $(this)

    # remove active from all siblings, add active to clicked
    $self.siblings().not('.divider-vertical').removeClass('active')
         .end().addClass('active')

  $navLinks[0...2].on 'click', (e) ->
    url = if $(this).text().toLowerCase() is 'new' then '/?sort=new' else '/'
    $('html, body').animate scrollTop: 0, 600

    # fadeout container and load in new posts
    $links_container.fadeOut 'slow', ->
      $.when( $links_container.load "#{url} .link_wraper > " )
       .then ->
            $link_container.fadeIn 'slow', ->
              attachVotes() if isLoggedIn()
  
  #kick it all off
  attachVotes() if isLoggedIn()
)(jQuery)
