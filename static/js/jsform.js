$(document).ready(function(){
    var maxField = 8; //Input fields increment limitation
    var wrapper = $('.field_wrapper'); //Input field wrapper
    var fieldHTML ='<div class="form-tab form-list" id="form index-1"><div class="left-col">Input Sample:<input type="text" name="sampel" id="sampel" placeholder="e.g. (1) RBD, (2) IBV, (3) Non-specific Sample, (4) Unknow Sample" style="width: -webkit-fill-available"/></div><div class="right-col">Input Concentration (ng/mL):<input type="text" name="konsen" id="konsen" placeholder="e.g. 12" style="width: -webkit-fill-available"></div><div style="margin: auto; padding: 1em;"><a href="javascript:void(0)" class="add_button"><span style="font-size: 1.5em"><i class="fas fa-plus-circle"></i></span></a></div><div style="margin: auto; padding-right: 1em;"><a href="javascript:void(0)" style="margin: auto;" class="remove_button"><span style="font-size: 1.5em;"  id="remove"><i class="fas fa-minus-circle"></i></span></a></div></div>';
    
    var x = 1; //Initial field counter is 1
    //Adjust indexes
    function adjustIndices(removedIndex) {
        var $forms = $('.form-list');
        $forms.each(function(i){
            var index = parseInt($(this).attr("id")[6]);
            var newIndex = index - 1;
            if (index < removedIndex){
                return true;
            };

            $(this).attr("id", "index-"+newIndex);
            $(this).find(".left-col input").attr("name", "sampel"+newIndex);
            $(this).find(".left-col input").attr("id", "sampel"+newIndex);
            $(this).find(".right-col input").attr("name", "konsen"+newIndex);
            $(this).find(".right-col input").attr("id", "konsen"+newIndex);
        });
    };

    //Once add button is clicked
    $(wrapper).on('click','.add_button', function(e){
        e.preventDefault();
        //Check maximum number of input fields
        if(x < maxField){ 
            x++; //Increment field counter
            $(wrapper).append(fieldHTML); //Add field html
            $(".form-list").last().attr("id", "index-"+x);
            $(".left-col input").last().attr("name", "sampel"+x);
            $(".left-col input").last().attr("id", "sampel"+x);
            $(".right-col input").last().attr("name", "konsen"+x);
            $(".right-col input").last().attr("id", "konsen"+x);    
        };
    });
    
    //Once remove button is clicked
    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        var removedIndex = parseInt($(this).parent('div').parent('div').attr("id")[6]);
        $(this).parent('div').parent('div').remove(); //Remove field html
        x--; //Decrement field counter
        adjustIndices(removedIndex);
    });
});

