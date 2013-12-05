$(function(){
  $("a.dropdown-toggle").click(function(e) {
      $(this).parent().toggleClass('open');
      e.preventDefault();
  })
})