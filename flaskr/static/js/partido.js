
$('#next').on('click', function () {
    $('#next').prop('disabled', true);
    $.ajax({
      method: "GET",
      url: ''+window.location.pathname,
      data: {['paginador']: $('#next').attr('name')},
      beforeSend: antesDeEnviar(),
      success: function (res) {
        res.map((e, k) => {
          paginacao(e);
          if (e.urlFoto != null && e.urlfoto != '') {
            return (
              $(`
                <div class="resultado pesquisa">
                <a href="/deputado/${e.id}">
                <div class="avatar"><img src="${e.urlFoto}"></div>        
                <h5>${e.nome}</h5>
                </a>
                </div>
                `).appendTo('#results')
            )
          }
        })
      },
      complete: function () {
        $("#loader-gif").hide()
        $('#next').prop('disabled', false);
      }
    })
  });
  
  
  
  $('#previous').on('click', function () {
    $('#previous').prop('disabled', true);
    $.ajax({
      method: "GET",
      url: ''+window.location.pathname,
      data: {['paginador']: $('#previous').attr('name')},
      beforeSend: antesDeEnviar(),
      success: function (res) {
        res.map((e, k) => {
          paginacao(e);
          if (e.urlFoto != null && e.urlfoto != '') {
            return (
              $(`
                <div class="resultado pesquisa">
                <a href="/deputado/${e.id}">
                <div class="avatar"><img src="${e.urlFoto}"></div>        
                <span class="name">${e.nome}</span>
                </a>
                </div>
                `).appendTo('#results')
            )
          }
        })
      },
      complete: function () {
        $("#loader-gif").hide()
        $('#previous').prop('disabled', false);
      }
    })
  });
  
  
  $('#first').on('click', function () {
    $('#first').prop('disabled', true);
    $.ajax({
      method: "GET",
      url: ''+window.location.pathname,
      data: {['paginador']: $('#first').attr('name')},
      beforeSend: antesDeEnviar(),
      success: function (res) {
        res.map((e, k) => {
          paginacao(e);
          if (e.urlFoto != null && e.urlfoto != '') {
            return (
              $(`
                <div class="resultado pesquisa">
                <a href="/deputado/${e.id}">
                <div class="avatar"><img src="${e.urlFoto}"></div>        
                <span class="name">${e.nome}</span>
                </a>
                </div>
                `).appendTo('#results')
            )
          }
        })
      },
      complete: function () {
        $("#loader-gif").hide()
        $('#first').prop('disabled', false);
      }
    })
  });
  
  
  $('#last').on('click', function () {
    $('#last').prop('disabled', true);
    $.ajax({
      method: "GET",
      url: ''+window.location.pathname,
      data: {['paginador']: $('#last').attr('name')},
      beforeSend: antesDeEnviar(),
      success: function (res) {
        res.map((e, k) => {
          paginacao(e);
          if (e.urlFoto != null && e.urlfoto != '') {
            return (
              $(`
                <div class="resultado pesquisa">
                <a href="/deputado/${e.id}">
                <div class="avatar"><img src="${e.urlFoto}"></div>        
                <span class="name">${e.nome}</span>
                </a>
                </div>
                `).appendTo('#results')
            )
          }
        })
      },
      complete: function () {
        $("#loader-gif").hide()
        $('#last').prop('disabled', false);
      }
    })
  });


  function antesDeEnviar (){
    deleteResultsChilds();
    $("#loader-gif").show();
    escondeBotoes ();
  }



function paginacao (e){
    if(e.linkNextPage != null && e.linkNextPage != ''){
      $('#next').attr('name', e.linkNextPage);
      $('#next').show();
    }
    if(e.linkPreviousPage != null && e.linkPreviousPage != ''){
      $('#previous').attr('name', e.linkPreviousPage);
      $('#previous').show();
    }
    if(e.linkFirstPage != null && e.linkFirstPage != ''){
      $('#first').attr('name', e.linkFirstPage);
      $('#first').show();
    }
    if(e.linkLastPage != null && e.linkLastPage != ''){
      $('#last').attr('name', e.linkLastPage);
      $('#last').show();
    }
  }

function escondeBotoes (){
    $('#next').hide();
    $('#previous').hide();
    $('#first').hide();
    $('#last').hide();
}

function deleteResultsChilds() {
  var result = document.getElementById('results');
  while (result.firstChild) {
    result.removeChild(result.firstChild);
  }
}
  
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