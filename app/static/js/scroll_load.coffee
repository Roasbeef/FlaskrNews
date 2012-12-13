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
       $new_posts.children().hide().appendTo('.link_wrapper').fadeIn(speed)


 $(window).on 'scroll', () ->

   if $(@).scrollTop() == $(document).height() - $(@).height()
     if scrollTimeout
       clearTimeout(scrollTimeout)
     
     scrollTimeout = setTimeout(scrollLoad, 200)

)(jQuery)
