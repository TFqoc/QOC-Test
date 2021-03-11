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
      url: "/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/mo_data/"+String(id),
      success: function( result ) {
        $( "#box_2" ).html(result);
      }
    });
  select(el,1);
}
function get_wo_data(el){
  id = el.getAttribute("model_id");
  $.ajax({
    url: "/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/wo_data/"+String(id),
    success: function( result ) {
      $( "#box_3" ).html(result);
    }
  });
  select(el,2);
}
function select(el, box){
  $("#box_"+String(box)).find(".selected").removeClass("selected");
  el.classList.add("selected");
}
//