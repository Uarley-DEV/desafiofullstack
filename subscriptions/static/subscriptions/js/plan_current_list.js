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
            url: '/subscriptions/plan_current_list/',
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
