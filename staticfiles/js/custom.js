function pager(i) {
    var form = document.getElementById('busqueda');
    form.setAttribute("method", "post");
    form.setAttribute("action", "");
    form['npage'].value=i;
    //alert(form.npage.value);
    form.submit();
}
function autoResize(obj){
    obj.style.height = 0;
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
//     var newheight;
//     var newwidth;

//     if(document.getElementById){
//         newheight = document.getElementById(id).contentWindow.document .body.scrollHeight;
//         newwidth = document.getElementById(id).contentWindow.document .body.scrollWidth;
//     }

//     document.getElementById(id).height = (newheight) + "px";
//     document.getElementById(id).width = (newwidth) + "px";
}

