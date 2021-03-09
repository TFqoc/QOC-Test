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