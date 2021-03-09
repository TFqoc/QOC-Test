function toggle_dropdown(el){
    var target = el.parentElement.parentElement.nextElementSibling;
    if (target.style.display == ''){
      target.style.display = 'none';
      el.className = 'fa fa-caret-right dropdown-content';
    }
    else{
      target.style.display = '';
      el.className = 'fa fa-caret-down dropdown-content';
    }
  }

function get_mo_data(el){
    id = el.getAttribute("model_id");
    $.ajax({
        url: "/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/objects/"+String(id),
        data: {
          zipcode: 97201
        },
        success: function( result ) {
          $( "#box_2" ).html( "<strong>" + result + "</strong>" );
        }
      });
}