$('#graph').ready( function () {
  
  let a = '<h3>Gastos nos últimos meses</h3>';
  var id = $('#idDeputado').attr('title');
    $.ajax({
      method: "GET",
      url: '/graph/deputado',
      data: {['deputado']: id},
      success: function (res) {
        $(`${a}${res}`).appendTo('#graph');
      },
      complete: function () {}
    })
  });

$('.number').each(function () {
  $(this).prop('Counter',0).animate({
      Counter: $(this).text()
  }, {
      duration: 1000,
      easing: 'swing',
      step: function (now) {
          $(this).text(Math.ceil(now));
      }
  });
});