function func(assets, input){
  input = input.toUpperCase()
  var tickers = document.getElementById("tickers")
  var new_html = ""
  for(var i=0; i < assets.length; i++){
    if(assets[i].match("[A-Z0-9]*" + input + "[A-Z0-9]*") != null){
      new_html += '<a href="/assets/"' + assets[i] + '/>' + assets[i] + "</a>";
      new_html += '\n\n';
    }
  }
  tickers.innerHTML = new_html;
  //console.log(tickers.innerHTML)
  //console.log(assets)
  //console.log(input)
}