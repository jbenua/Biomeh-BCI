try{
if (cookiestate == 0 && document.cookie.indexOf('ar_g2') == -1){
	sC('ar_g2', 1, 1000*60*60*24*7);
	document.write('<img src="https://cm.g.d'+'oubleclick.net/pixel?google_nid=ADR&google_cm&google_sc">');
}
if (cid && http && cookiestate == 0 && document.cookie.indexOf('ar_ord') == -1){
		sC('ar_ord', 1, 1000*60*60*24);
		document.write('<img src="//a'+'d.mail.ru/cm.gif?p=23&id='+encodeURIComponent(cid)+'">');
}
if (cid && cookiestate == 0 && document.cookie.indexOf('ar_ya') == -1){
		sC('ar_ya', 1, 1000*60*60*24);
		var makeCRCTable = function(){
			var c;
			var crcTable = [];
			for(var n =0; n < 256; n++){
				c = n;
				for(var k =0; k < 8; k++){
					c = ((c&1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1));
				}
				crcTable[n] = c;
			}
			return crcTable;
		}

		var crc32 = function(str) {
			var crcTable = window.crcTable || (window.crcTable = makeCRCTable());
			var crc = 0 ^ (-1);

			for (var i = 0; i < str.length; i++ ) {
				crc = (crc >>> 8) ^ crcTable[(crc ^ str.charCodeAt(i)) & 0xFF];
			}

			return (crc ^ (-1)) >>> 0;
		}; 
		if ((/MSIE (\d+\.\d+);/.test(navigator.userAgent)) || (document.body.style.msTextCombineHorizontal !== undefined)){
		var usAge = window.navigator.userAgent;
		usAge=usAge.split(" ");
		for(var i=0; i<usAge.length; i++) {
		  if(usAge[i].indexOf('Trident')!==-1){var strt = i}
		  if(usAge[i].indexOf('rv:')!==-1){var strend = i}
		}
		var usAg = [];
		if (strt){
		for(var i=0; i<=strt; i++) {
		  usAg.push(usAge[i]);
		}}
		if (strend){
		for(var i=strend; i<usAge.length; i++) {
		  usAg.push(usAge[i]);
		}}
		usAg = usAg.join(' ');
		if(strt && !strend){usAg = usAg.slice(0,-1)+')';}}else{var usAg = window.navigator.userAgent;}
		var sep = '.', ip = ip.split(sep), cidsep=cid.slice(1).replace('==', ''); ip = ip[0]+'.'+ip[1]+'.'+ip[2];
		var hash = crc32(ip+window.location.href+usAg+''+cidsep+'6456cb2ae565cb18dceaa12d1898837c');
		document.write('<img src="//an.yandex.ru/setud/adriver/'+cidsep+'?sign='+hash+'">');
}
}catch(e){}