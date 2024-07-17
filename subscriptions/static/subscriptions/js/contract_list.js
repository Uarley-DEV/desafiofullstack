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

var tab_contract = function() {
    var kt_contract = function() {
        
        var table = $('#kt_contract');
        
        if ($.fn.DataTable.isDataTable('#kt_contract')) {
            table.DataTable().destroy();
        }

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
            autoWidth: true,  
            language: {
                processing: "Processamento em andamento...",
                search: "Pesquisar:",
                lengthMenu: "MENU registros por página",
                infoEmpty: "Mostrando 0 até 0 de 0 registros",
                infoFiltered: "(Filtrados de MAX registros)",
                infoPostFix: "",
                loadingRecords: "Carregando registros...",
                zeroRecords: "Nenhum registro encontrado",
                emptyTable: "Nenhum registro encontrado",
                paginate: {
                    first: "Primeiro",
                    previous: "Anterior",
                    next: "Avançar",
                    last: "Último"
                },
                aria: {
                    sortAscending: ": Ordenar coluna por ordem crescente",
                    sortDescending: ": Ordenar coluna por ordem decrescente"
                }
            },
            ajax: {
                url: '/subscriptions/contract_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[0, 'asc']],
            columns: [
                {data: 'contract_id'},
                {data: 'plan_name'},
                {data: 'plan_value'},
                {data: 'credits'},
                {data: 'payment_date'},
                
            ],
                columnDefs: [
                    {
                        targets: [1, 2, 3, 4],
                        className: 'text-center',
                    },
                    {
                        targets: [2, 3],
                        render: function(data, type, row) {
                            return parseFloat(data).toFixed(2).replace('.', ',');
                    }
                },
            ],
        });  
    };

    return {
        init: function() {
            kt_contract();
        },
    };
}();

jQuery(document).ready(function() {
    tab_contract.init();
});