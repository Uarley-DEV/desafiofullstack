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

var tab_user = function() {
    var kt_user = function() {
        
        var table = $('#kt_user');
        
        if ($.fn.DataTable.isDataTable('#kt_user')) {
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
            autoWidth: true,  // Permitir que a tabela ajuste automaticamente a largura
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
                url: '/subscriptions/user_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[0, 'asc']],
            columns: [
                {data: 'user_id'},
                {data: 'user_name'},
                {data: 'user_email'},
                {data: 'address'},
                {data: 'phone'},
            ],
            columnDefs: [
                {
                    targets: [1, 2, 3, 4],
                    className: 'text-center',
                },
            ],
        });  
    };

    return {
        init: function() {
            kt_user();
        },
    };
}();

jQuery(document).ready(function() {
    tab_user.init();
});