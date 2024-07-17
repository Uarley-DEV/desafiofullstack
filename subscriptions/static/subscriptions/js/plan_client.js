
"use strict";

$.fn.dataTable.Api.register('column().title()', function() {
    return $(this.header())[0].dataset.field;
}); 

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

var tab_plan = function() {
    var kt_plan = function() {
        $.ajax({
            url: '/subscriptions/plan_list/',
            type: 'POST',
            dataType: 'json', 
            dataSrc: 'dados', 
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()  
            },
            success: function(response) {
                var data = response.dados; 
                $('#card_deck').empty();

                $.each(data, function(index, item) {
                    var col = $('<div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4"></div>'); 
                    var card = $('<div class="card"></div>').css({
                        'background-color': '#fff',
                        'margin': '0 10px 10px 0', 
                        'width': '250px', 
                        'height': '250px' 
                    });
                    var cardBody = $('<div class="card-body"></div>').css('color', '#333'); 
                    cardBody.append('<h5 class="card-title text-left" style="background-color: #e65729; color: #fff">' + item.plan_name + '</h5>');
                    cardBody.append('<p class="card-text" style="font-weight: bold;">Preço: <br><span class="plan-value" style="font-size: 1.23em; font-weight: bold;">R$ ' + item.plan_value.toFixed(2).replace('.', ',') + '</span> <span style="font-size: 0.8em;">/mês</span></p>');
                    cardBody.append('<p class="card-text">Armazenamento: <br><span class="plan-storage" style="font-size: 1.23em; font-weight: bold;">' + item.plan_storage +  ' GB </b></span></p>');

                    cardBody.append('\
                         <a href="/subscriptions/payment_pix/' + item.plan_id + '/" class="btn btn-light-success btn-icon btn-circle"\
                            data-toggle="tooltip" data-placement="bottom" title="Contratar">\
                            <i class="flaticon2-contract"></i>\
                        </a>\
                    ');

                    card.append(cardBody);
                    col.append(card);
                    $('#card_deck').append(col); // Adiciona diretamente à div de cards
                });
            },
            error: function(xhr, status, error) {
                console.error('Erro na requisição:', error);
            }
        });
    };

    return {
        init: function() {
            kt_plan();
        },
        reload: function() {
            kt_plan();
        }
    };
}();

jQuery(document).ready(function() {
    tab_plan.init()
    
});

function abrir_modal_plan(){
    $('#plan_btn_salvar').val('insert');
    $('#plan_name').val('');
    $('#plan_value').val('');
    $('#plan_storage').val('');
    $('#plan_quotas').val('');
    $('#frm_plan_modal').modal('show');
}

function plan_add(){
    var url
    if($('#plan_btn_salvar').val() == 'update'){
        url = '/subscriptions/plan_edt/'
    }else{
        url = '/subscriptions/plan_add/'
    }

    var frm_plan = new FormData(document.getElementById('frm_plan'));

    $.ajax({
        method: 'POST',
        url: url,
        data: frm_plan,
        contentType: false,
        cache: false,
        processData: false,
        beforeSend: function() {
            Swal.fire({
                title: "Carregando os dados",
                text: "Aguarde ...",
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                didOpen: function() {            
                    Swal.showLoading();
                }
            })
        },
    })
    .done(function(data,  textStatus, jqXHR){
        if (jqXHR.status === 200 && jqXHR.readyState === 4){
            tab_plan.reload();
            $('#frm_plan_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}


function plan_contract(plan_id){
    $.getJSON('/subscriptions/plan_atb/',
        {
            plan_id: plan_id
        }
    ).done(function (item) {
        $('#plan_id').val(item.plan_id);
        $('#plan_value').val(item.plan_value);
        $('#plan_name').val(item.plan_name);
        $('#plan_storage').val(item.plan_storage);
        $('#plan_quotas').val(item.plan_quotas);
        $('#plan_btn_salvar').val('update');
        $('#frm_plan_modal').modal('show');
        tab_plan.init();
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}

function plan_del(plan_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + plan_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("plan_id", plan_id);

            $.ajax({
                method: 'POST',
                url: '/subscriptions/plan_del/',
                data:  dados,
                contentType: false,
                cache: false,
                processData: false,
                beforeSend: function() {
                    Swal.fire({
                        title: "Operação em andamento",
                        text: "Aguarde ...",
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        allowEnterKey: false,
                        didOpen: function() {            
                            Swal.showLoading();
                        }
                    })
                },
            })
            .done(function(data,  textStatus, jqXHR){
                console.log(jqXHR);
                if (jqXHR.status === 200 && jqXHR.readyState === 4){
                    tab_plan.reload();
                    $('#frm_plan_modal').modal('hide');
                    Swal.close();
                }
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                Swal.close();
                Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
            });
        }
    });
};