if($.cookie("css")) {
   $("#theme").attr("href",$.cookie("css"));
}

if($.cookie("css_name")) {
   document.title = 'Design 3 - ' + $.cookie("css_name");
}
 
$(document).ready(function() { 
   $("#nav li a").click(function() { 
      $("#theme").attr("href",$(this).attr('rel'));
      document.title = 'Design 3 - ' + $(this).text();
      $.cookie("css",$(this).attr('rel'), {expires: 365, path: '/'});
      $.cookie("css_name",$(this).text(), {expires: 365, path: '/'});
      return false;
   });
	      
   $(".trigger").click(function(){
      $(".panel").toggle("fast");
      $(this).toggleClass("active");
      return false;
   });
});
