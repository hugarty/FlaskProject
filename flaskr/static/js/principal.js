if ( $('#results').children().length > 0 ) {
  $('#map').hide();
  $('.container').css('flex-direction', 'column');
}
function deleteResultsChilds() {
  var result = document.getElementById('results');

  while (result.firstChild) {
    result.removeChild(result.firstChild);
  }
}

//trata as alterações feitas no Radio e passa para o select
$('input[type="radio"]').on('change', function () {
  if (!this.value) {
  } else {
    if ($('input[type="radio"]:checked').val() == "deputados") {
      $('select[name="cargo"]').val('Deputados');
      $('input[name="name"]').attr("placeholder", "Nome do deputado");
    }
    else {
      $('select[name="cargo"]').val('Partidos');
      $('input[name="name"]').attr("placeholder", "Sigla do partido");
    }
    $('#type').hide()
    $('#name').show()
  }
})

//trata as alterações feitas no select e passa para o radio
$('select[name="cargo"]').on('change', function () {
  if (!this.value) {
  } else {
    if ($('select[name="cargo"]').val() == "Deputados") {
      $('#s-option').prop('checked', false);
      $('#f-option').prop('checked', true);
      $('input[name="name"]').attr("placeholder", "Nome do deputado");
    }
    else {
      $('#f-option').prop('checked', false);
      $('#s-option').prop('checked', true);
      $('input[name="name"]').attr("placeholder", "Sigla do partido");
    }
    $('#type').hide()
    $('#name').show()
  }
})

$('#search').on('click', function () {
  $('#map').hide();
  $('.container').css('flex-direction', 'column');
  $('#search').prop('disabled', true);
  var route = $('input[type="radio"]:checked').val();
  var name = $('input[name="name"]').val();
  var teveRetorno = false;
  $.ajax({
    method: "GET",
    url: '/',
    data: { [route]: name },
    beforeSend: antesDeEnviar(),
    success: function (res) {
      res.map((e, k) => {
        teveRetorno = true;
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
        } else {
          if (e.semDados == 'semDados'){
            return (
              $(`
              <div class="resultado pesquisa">
              <h4>Pesquise pela sigla inteira do partido</h4>
              </div>
              `).appendTo('#results')
            )
          }else{
            return (
              $(`
              <div class="resultado pesquisa">
              <a href="/partido/${e.id}">        
              <span class="name">${e.sigla}</span>
              </a>
              </div>
              `).appendTo('#results')
            )
          }
        }
      })
    },
    complete: function () {
      $("#loader-gif").hide()
      $('#search').prop('disabled', false);
      $('#next').prop('disabled', false);
      if (!teveRetorno) {
        $('#semRetorno').show();
      }
    }
  })
})



$('#next').on('click', function () {
  $('#next').prop('disabled', true);
  $.ajax({
    method: "GET",
    url: '/',
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
      $('#next').prop('disabled', false);
    }
  })
});



$('#previous').on('click', function () {
  $('#previous').prop('disabled', true);
  $.ajax({
    method: "GET",
    url: '/',
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
    url: '/',
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
    url: '/',
    data: {['paginador']: $('#last').attr('name')},
    beforeSend: antesDeEnviar(),
    success: function (res) {
      res.map((e, k) => {
        paginacao(e);
        if (e.urlFoto != null && e.urlfoto != '') {
          return (
            $(`
              <div>
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
  $('#semRetorno').hide();
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

