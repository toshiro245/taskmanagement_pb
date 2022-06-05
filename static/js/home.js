$(function () {

    'user strict';

    // グラフ描画定義
    var type = 'bar';
    var options = {
        legend: {
            display: false
        },
        animation: {
            duration: 1000,
        },
        scales: {
            xAxes: [{
                ticks: {
                    fontColor: "black",
                    fontSize: 14,
                    callback: function(value, index, values){
                        return [value.substr(5,2) + '/' + value.substr(8,2)]
                    } 
                },
                gridLines: {
                    color: 'rgba(48, 48, 47, 0.3)',
                },
            }],
            yAxes: [{
                ticks: {
                    fontColor: "black",
                    fontSize: 14,
                    suggestedMin: 0,
                    suggestedMax: 1800,
                    stepSize: 1800,
                    callback: function(value, index, values){
                        return String(value / 3600) + 'hours'
                    }
                },
                gridLines: {
                    color: 'rgba(48, 48, 47, 0.3)',
                },
            }],
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem, data){
                    let value = tooltipItem.yLabel
                    // let value = tooltipItem.value;
                    // let index = tooltipItem.datasetIndex;
                    let label = data.datasets[0].label;
                    return label + ' ' + ':' + ' ' + String(Math.floor(value / 3600)) + 'hour' + ' ' + String(Math.floor(value%3600/60)) + 'min'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
    };

    // Task Record Graph表示
    $('.item').click(function () {
        var result = $(this).css('border-color');
        var task_id = $(this).attr('name');
        var task_name = $(this).attr("value");
        $('#overlay, .modal-window').fadeIn();
        $('.modal-window').css('background-color', result);
        $('#hidden-delete').val(task_id);
        $('.task-title').text(task_name);
        $('#task-edit-btn').attr("href", `task_update/${task_id}`)
        $('#task-start-btn').attr("href", `task_conduct/${task_id}`)

        // グラフ用の必要情報取得Ajax
        var token = $('input[name="csrfToken"]').attr('value');
        $.ajaxSetup({
            beforeSend: function(xhr){
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        })
        $.ajax({
            type: "POST",
            url: "/taskmanagement/get_record/",
            data: {
                'task_id': task_id,
                'offset': '7',
            },
            dataType: 'json',
            success: function(response){
                var data = response.data
                
                $('#my_chart').remove();
                $('.canvas-container').append("<canvas id='my_chart'></canvas>");
                var ctx = document.getElementById('my_chart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: type,
                    data: data,
                    options: options,
                });

            }
        }); 

    });

    $('.close-btn, #overlay').click(function () {
        $('#overlay, .modal-window').fadeOut();
    });


    // Task Record Graph表示-Period変更時
    $('.period-btn').click(function () {
        $('.period-btn').removeClass('btn-active');
        $(this).addClass('btn-active');
        var task_id = $('#hidden-delete').val();
        var offset = $(this).val()

        // グラフ用の必要情報取得Ajax
        var token = $('input[name="csrfToken"]').attr('value');
        $.ajaxSetup({
            beforeSend: function(xhr){
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        })
        $.ajax({
            type: "POST",
            url: "/taskmanagement/get_record/",
            data: {
                'task_id': task_id,
                'offset': offset,
            },
            dataType: 'json',
            success: function(response){
                var data = response.data
                
                $('#my_chart').remove();
                $('.canvas-container').append("<canvas id='my_chart'></canvas>");
                var ctx = document.getElementById('my_chart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: type,
                    data: data,
                    options: options,
                });
            }
        }); 
    });
});


// Delete modal
$(function(){

    $('#task-delete-btn').click(function(){
        $('#delete-modal-wrapper').fadeIn();
    });

    // cancelが押された時の処理
    $('.cancel-btn').click(function(){
        $("#delete-modal-wrapper").fadeOut();
    });

});

// Delete Record modal
$(function(){
    $('.record-delete-btn').click(function(){
        $('#delete-record-modal-wrapper').fadeIn();
        var task_record_id = $(this).val();
        $('#hidden-record-delete').val(task_record_id);

    });

    // cancelが押された時の処理
    $('#delete-record-cancel-btn').click(function(){
        $("#delete-record-modal-wrapper").fadeOut();
    });

});

