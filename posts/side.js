var h2_headings = document.querySelectorAll('h2');
var table = document.getElementById("navigation-bar");
if (h2_headings.length > 0) {
  var inner = "";
  inner += '<ul>\n';
  for (var i = 0; i < h2_headings.length; i++) {
    var id = h2_headings[i].id;
    if (id == '') continue;
    inner  += '<li><a onmouseover="_focus('+"'"+h2_headings[i].innerHTML+"'"+')" onmouseout="_unfocus()" class="active" href="'+ "#"+id +'">'+ h2_headings[i].textContent +'</a></li>\n';
  }
  inner += '</ul>\n';
}
table.innerHTML += inner;

function _focus(id) {
  var elems = document.getElementsByClassName('active');
  for (var i = 0; i < elems.length; i++) {
    elems[i].setAttribute('style', 'color: #000000;');
    if (elems[i].innerHTML == id) {
      elems[i].setAttribute('style', 'color: #0055bb;');
    }
  }
}
function _unfocus() {
  var elems = document.getElementsByClassName('active');
  for (var i = 0; i < elems.length; i++) {
    elems[i].setAttribute('style', 'color: #000000;');
  }
}