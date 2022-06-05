$(function(){

    'user strict';

    const timer = document.getElementById('timer');
    const start = document.getElementById('start');
    const stop = document.getElementById('stop');
    const reset = document.getElementById('reset');
    const record = document.getElementById('record');

    let startTime;
    let timeoutId;
    let elapsedTime = 0;
    const gmt = new Date().getTimezoneOffset() / 60;

    function countUp() {
        const d = new Date(Date.now() - startTime + elapsedTime);
        const h = String(d.getHours() + gmt).padStart(2, '0');
        const m = String(d.getMinutes()).padStart(2, '0');
        const s = String(d.getSeconds()).padStart(2, '0');
        timer.textContent = `${h}:${m}:${s}`

        timeoutId = setTimeout(()=>{
            countUp();
        }, 1000);
    }

    function setButtonStateInitial() {
        start.classList.remove('inactive');
        stop.classList.add('inactive');
        reset.classList.add('inactive');
        record.classList.add('inactive');
    }

    function setButtonStateRunning() {
        start.classList.add('inactive');
        stop.classList.remove('inactive');
        reset.classList.add('inactive');
        record.classList.add('inactive');
    }

    function setButtonStateStopped() {
        start.classList.remove('inactive');
        stop.classList.add('inactive');
        reset.classList.remove('inactive');
        record.classList.remove('inactive');
    }

    setButtonStateInitial();


    start.addEventListener('click', ()=>{
        if (start.classList.contains('inactive') === true) {
            return;
        }
        setButtonStateRunning();
        startTime = Date.now();
        console.log()
        countUp();
    });

    stop.addEventListener('click', ()=>{
        if (stop.classList.contains('inactive') === true) {
            return;
        }
        setButtonStateStopped();
        clearTimeout(timeoutId);
        elapsedTime += Date.now() - startTime;
    });

    reset.addEventListener('click', ()=>{
        if (reset.classList.contains('inactive') === true) {
            return;
        }
        setButtonStateInitial();
        timer.textContent = '00:00:00';
        elapsedTime = 0;
    });

});



$(function () {
    $('#record').click(function () {
        if ($(this).hasClass("inactive") === true) {
            return;
        }
        var token = $('input[name="csrfToken"]').attr('value');
        $.ajaxSetup({
            beforeSend: function(xhr){
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        })

        var task_id = $('.task-title').attr('name');
        $.ajax({
            type: "POST",
            url: "/taskmanagement/task_record/",
            data: {
                'record': $('#timer').text(),
                'task_id': task_id,
            },
            dataType: 'json',
            success: function(response){
                $('#reset').trigger("click");
                $("#loading-modal").fadeIn(function(){
                    $(this).delay(1500).fadeOut();
                });
                setInterval(function(){
                    $('#success-modal-wrapper').fadeIn();
                }, 1500);
            }
        });   
    });
});


// loading modal
(() => {
    class IconDrawer {
        constructor(canvas) {
            this.ctx = canvas.getContext('2d');
            this.width = canvas.width;
            this.height = canvas.height;
            this.r = 60;
        }

        draw(angle) {
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            this.ctx.fillRect(0, 0, this.width, this.height);


            this.ctx.save()
            this.ctx.translate(this.width / 2, this.height / 2)
            this.ctx.rotate(Math.PI / 180 * angle);

            this.ctx.beginPath();
            this.ctx.moveTo(0, -this.r - 5);
            this.ctx.lineTo(0, -this.r + 5);
            this.ctx.strokeStyle = 'black';
            this.ctx.lineWidth = 6;
            this.ctx.stroke();

            this.ctx.restore();

        }
    }

    class Icon {
        constructor(drawer){
            this.drawer = drawer;
            this.angle = 0;
        }

        draw() {
            this.drawer.draw(this.angle);
        }


        update() {
            this.angle += 12;
        }

        run() {
            this.update();
            this.draw();

            setTimeout(() => {
                this.run();
            }, 100)
        }
    }

    const canvas = document.querySelector('canvas');
    if (typeof canvas.getContext === 'undefined') {
        return
    }

    const icon = new Icon(new IconDrawer(canvas));
    icon.run()

 })();
