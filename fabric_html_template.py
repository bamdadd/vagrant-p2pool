def html_doc():
  return """<!DOCTYPE html>
<html lang="en">
  <head>
    <style type="text/css">
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, #extras, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure,
#extras, header, hgroup, menu, nav, section {
  display: block;
}
html {
  background:rgb(197,209,217);
}
body {
  line-height: 1;
  padding:1em;
}
ol, ul {
  list-style: none;
}
blockquote, q {
  quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
  content: '';
  content: none;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
}
html { background:white; }
body {
  background:white;
  clear:both;
	line-height:1;
  margin:0 auto;
  overflow:none;
  padding-right:225px;
  width:670px;
}
h2 { font-size:1.3em; line-height: 1.618em; }
li { border:2px solid; border-left-width:25px; line-height:1.618em; list-style:none; padding-left:1em; border-radius:7px; -webkit-border-radius:7px; margin-bottom:2px; }
.info { border-color:#BFF468; }
.notice { border-color:#2E51A5; }
.err { border-color:#A53C25; }
pre { line-height:1.2em; font-family:monospace; overflow:auto; margin-bottom:1.309em; }
pre span { display:block; line-height:1.2em; float:left; clear:both; width:100%; }
.add { background-color:#99ff99; }
.remove { background-color:#ff9999; }
ul li a { display:block; text-decoration:none; color:black; }
#results {
  float:left;
  width:100%;
}
#legend {
  float:left;
  margin-top:3.1em;
  margin-right:-100%;
  padding-left:25px;
  position:relative;
  width:200px;
}
    </style>
  </head>
  <body>
<div id="results"><h2>Puppet Run: $host</h2><ul><pre>$content</pre></div>
<div id="legend">
<ul>
  <li class="err"><a href="#" onclick="return toggle('err', this);">err</a>
  <li class="info"><a href="#" onclick="return toggle('info', this);">info</a>
  <li class="notice"><a href="#" onclick="return toggle('notice', this);">notice</a>
</ul>
</div>

<script type="text/javascript">
function toggle(klass, button) {
  // scope to results section
  results = document.getElementById('results');
  // get all list elements by class name
  lis = results.getElementsByClassName(klass);
  for(i = 0; i < lis.length; i++) {
    lis[i].style.display = (lis[i].style.display != 'none') ? 'none' : 'block';
  }
  button.style.color = (button.style.color != '') ? '' : '#999';
  return false;
}

function calculate(container, dest) {
  legend = document.getElementById(dest);
  results = document.getElementById(container);
  types = ['err', 'info', 'notice'];
  for(index in types) {
    type = types[index];
    count = results.getElementsByClassName(type).length;
    legend.getElementsByClassName(type)[0].children[0].innerHTML = type + ' (' + count + ')';
  }
}

calculate('results', 'legend');
</script>
"""