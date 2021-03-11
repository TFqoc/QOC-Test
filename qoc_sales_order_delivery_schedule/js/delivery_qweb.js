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
  next_box = String(next_box_id(el));
  current_box = get_box_id(el);

  $.ajax({
      url: "/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/mo_data/"+String(id),
      success: function( result ) {
        if (next_box % 2 == 1 && $('#box_'+(current_box+2)).length == 0){
          // Create new row
          id1 = current_box+2;
          id2 = id1+1;
          $("#page_container").append('<div class="row justify-content-around mb-4"><div class="col"><div class="ds_card" id="box_'+id1+'"><span>Content</span></div></div><div class="col"><div class="ds_card" id="box_'+id2+'"><span>Content</span></div></div></div>');
        }
        $( "#box_"+next_box).html(result);
      }
    });
    console.log("Next: "+next_box+"\nCurrent: "+current_box);
  select(el,current_box);
}
function get_wo_data(el){
  id = el.getAttribute("model_id");
  next_box = String(next_box_id(el));
  current_box = get_box_id(el);

  $.ajax({
    url: "/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/wo_data/"+String(id),
    success: function( result ) {
      if (next_box % 2 == 1 && $('#box_'+(current_box+2)).length == 0){
        // Create new row
        id1 = current_box+2;
        id2 = id1+1;
        $("#page_container").append('<div class="row justify-content-around mb-4"><div class="col"><div class="ds_card" id="box_'+id1+'"><span>Content</span></div></div><div class="col"><div class="ds_card" id="box_'+id2+'"><span>Content</span></div></div></div>');
      }
      $( "#box_"+next_box).html(result);
    }
  });
  console.log("Next: "+next_box+"\nCurrent: "+current_box);
  select(el,current_box);
}
function select(el, box){
  $("#box_"+String(box)).find(".selected").removeClass("selected");
  el.classList.add("selected");
}
function get_box_id(el){
  return $(el).closest(".ds_card").attr('id').substring(4);
}
function next_box_id(el){
  return eval($(el).closest(".ds_card").attr('id').substring(4)+" + 1");
}