#TODO:
# attach votes to new posts
(($) ->
 navLinks = $('.nav:eq(0) > li').not('.divider-vertical')[0...2]

 scrollLoad = ->
   wantsHot      = $(navLinks[0]).hasClass('active')
   $cur_info     = $('#cur_info').detach()
   cursor_string = $cur_info.data('cur_string')
   page_num      = parseInt($cur_info.data('page_num')) + 1
   more_to_load  = $cur_info.data('more_content')
   $new_posts    = $('<div>')
   speed         = 2000
   url           = '/'

   return false unless more_to_load

   $new_posts.load "#{url} .link_wrapper > ",
     cur_string: cursor_string, page_num: page_num, sort: if wantsHot then 'hot' else 'new',
     () ->
       console.log $new_posts
       $new_posts.children().hide().appendTo('.link_wrapper').fadeIn(speed)
       console.log $cur_info

  past_point = false

  $(window).on 'scroll', () ->
    doc_height  = $(document).height()
    scroll_pos  = $(@).scrollTop()
    load_point  = doc_height / 4

    unless past_point
      if scroll_pos > load_point
        past_point = true
        console.log 'try'
        $.when( scrollLoad() ).then () ->
          past_point = false
          console.log 'good loop'

)(jQuery)
