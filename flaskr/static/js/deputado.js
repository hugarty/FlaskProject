$('#graph').ready( function () {
  
  let a = '<h4>Quantidade de gastos do Deputado só nos ultimos dois meses</h4>';
  var id = $('#idDeputado').attr('title');
    $.ajax({
      method: "GET",
      url: '/graph/deputado',
      data: {['deputado']: id},
      success: function (res) {
        $(`${a}
        ${res}`).appendTo('#graph')
      },
      complete: function () {}
    })
  });