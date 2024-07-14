
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
        
        var table = $('#kt_plan');
        // begin first table
        table.on('processing.dt', function (e, settings, processing) {
            if (processing) {
                Toast.fire({
                    icon: 'success',
                    title: 'Sucesso! Carregando os dados ...'
                });
            } else {
                Toast.close();
            }
        }).DataTable({
            responsive: true,
            processing: true,
            pageLength: 10,
            paging: false,
            language: {
                processing:     "Processamento em andamento...",
                search:         "Pesquisar:",
                lengthMenu:     "MENU registros por página",
                info:           "Mostrando de START até END de TOTAL registros",
                infoEmpty:      "Mostrando 0 até 0 de 0 registros",
                infoFiltered:   "(Filtrados de MAX registros)",
                infoPostFix:    "",
                loadingRecords: "Carregando registros...",
                zeroRecords:    "Nenhum registro encontrado",
                emptyTable:     "Nenhum registro encontrado",
                paginate: {
                    first:      "Primeiro",
                    previous:   "Anterior",
                    next:       "Avançar",
                    last:       "Último"
                },
                aria: {
                    sortAscending:  ": Ordenar coluna por ordem crescente",
                    sortDescending: ": Ordenar coluna por ordem decrescente"
                }
            },
            ajax: {
                url: '/subscriptions/plan_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'plan_id'},
                {data: 'plan_nome'},
                {data: 'plan_cor'},
                {data: 'plan_ativo'},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                {
                targets: [2],
                type: "text",
                render: function(data) {
                    if (data.startsWith('#') && (data.length === 7 || data.length === 4)) {
                        return '<div style="width: 30px; height: 30px; background-color: ' + data + ';"></div>';
                    } else {
                        return data;
                    }
                }
                },  
                {
                    targets: [3],
                    type: "text",
                    render: function(data) {
                        if (data === true) {
                            return '<span class="btn btn-text-success btn-hover-light-success font-weight-bold mr-2">Sim</span>';
                        } else {
                            return '<span class="btn btn-text-danger btn-hover-light-danger font-weight-bold mr-2">Não</span>';
                        }
                    },
                },                
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="plan_edt(' + row.plan_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="plan_del(' + row.plan_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" title="Remover">\
                                <i class="flaticon-delete"></i>\
                            </button>\
                        ';
                    },
                },
            ],
        });  
    };

    return {
        //main function to initiate the module
        init: function() {
            kt_plan();
        },
    };
}();



jQuery(document).ready(function() {
    tab_plan.init()
    
});

function abrir_modal_plan(){
    $('#plan_btn_salvar').val('insert');
    $('#plan_nome').val('');
    $('#plan_cor').val('');
    $('#plan_ativo').prop('checked', false);
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
            $('#kt_plan').DataTable().ajax.reload();
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
