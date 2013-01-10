$(function(){


    var Painter = function($canvas){
        var canvas = $canvas[0]; 
        var context = canvas.getContext('2d')
        
        canvas.onselectstart =function(){return false;}
        
        this._drawing = false;
        this._last_x = null;
        this._last_y = null;

        var painter_rect = canvas.getBoundingClientRect();

        var painter = this;
    
        function drawPoint(x, y, isclick){
            isclick = isclick || false;
            x = x - painter_rect.left;
            y = y - painter_rect.top;
            if (isclick){
                context.moveTo(x, y-0.5)
            }else{
                context.moveTo(painter._last_x, painter._last_y)
            }
            context.lineTo(x, y)
            context.stroke()
            painter._last_x = x
            painter._last_y = y
        }

        $canvas.mousemove(function(e){
            if (painter._drawing){

                drawPoint(e.pageX, e.pageY)
            }
        });

        

        $canvas.mousedown(function(e){
            if (e.which == 1){
                painter._drawing=true; 
                drawPoint(e.pageX, e.pageY, true)}
        }).mouseup(function(e){
            if (e.which == 1){painter._drawing=false}
        })

    }

    var painter = new Painter($('canvas#paper'));

})
