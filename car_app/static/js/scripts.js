$(document).ready(function(){
    $("#show_model").click(function(){
        truck_model_select_value = truck_model_select.value; 
        alert("POPOP  "+ truck_model_select.value);
        alert("POPOP   - "+ truck_model_select.value);
        
        $.post('/trucks/index/', {'truck_model_select_value': truck_model_select_value}, function(data){
          $(".table table-hover").html(data);
          alert("data   =   " + data);
        
        
        });
        
        
        
    });
    
    
    
    function checkForReload(){
      var selected_model_id = 0;
      alert('selected_model_id = ' + selected_model_id);
    }
    
    
});


