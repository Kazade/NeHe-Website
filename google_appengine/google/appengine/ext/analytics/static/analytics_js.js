/* Copyright 2008-9 Google Inc. All Rights Reserved. */ (function(){var k,m=this,n=function(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b},q=function(a){return"string"==typeof a},r=function(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var b=c.slice();b.push.apply(b,arguments);return a.apply(this,b)}},aa=Date.now||function(){return+new Date},s=function(a,b){var c=a.split("."),e=m;c[0]in e||!e.execScript||e.execScript("var "+c[0]);for(var d;c.length&&(d=c.shift());)c.length||void 0===b?e=e[d]?e[d]:e[d]={}:e[d]=b},t=function(a,b){function c(){}
c.prototype=b.prototype;a.n=b.prototype;a.prototype=new c;a.q=function(a,c,f){var g=Array.prototype.slice.call(arguments,2);return b.prototype[c].apply(a,g)}};var u=function(a){Error.captureStackTrace?Error.captureStackTrace(this,u):this.stack=Error().stack||"";a&&(this.message=String(a))};t(u,Error);var ba=function(a,b){for(var c=a.split("%s"),e="",d=Array.prototype.slice.call(arguments,1);d.length&&1<c.length;)e+=c.shift()+d.shift();return e+c.join("%s")},w=function(a){a=String(a);var b=a.indexOf(".");-1==b&&(b=a.length);b=Math.max(0,2-b);return Array(b+1).join("0")+a},x=function(a,b){return a<b?-1:a>b?1:0};var y=function(a,b){b.unshift(a);u.call(this,ba.apply(null,b));b.shift()};t(y,u);var z=function(a,b,c){if(!a){var e=Array.prototype.slice.call(arguments,2),d="Assertion failed";if(b)var d=d+(": "+b),f=e;throw new y(""+d,f||[]);}};var A=Array.prototype,B=A.indexOf?function(a,b,c){z(null!=a.length);return A.indexOf.call(a,b,c)}:function(a,b,c){c=null==c?0:0>c?Math.max(0,a.length+c):c;if(q(a))return q(b)&&1==b.length?a.indexOf(b,c):-1;for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},ca=A.forEach?function(a,b,c){z(null!=a.length);A.forEach.call(a,b,c)}:function(a,b,c){for(var e=a.length,d=q(a)?a.split(""):a,f=0;f<e;f++)f in d&&b.call(c,d[f],f,a)},da=A.filter?function(a,b,c){z(null!=a.length);return A.filter.call(a,b,
c)}:function(a,b,c){for(var e=a.length,d=[],f=0,g=q(a)?a.split(""):a,h=0;h<e;h++)if(h in g){var v=g[h];b.call(c,v,h,a)&&(d[f++]=v)}return d},D=function(a){var b=a.length;if(0<b){for(var c=Array(b),e=0;e<b;e++)c[e]=a[e];return c}return[]},ea=function(a,b,c){z(null!=a.length);return 2>=arguments.length?A.slice.call(a,b):A.slice.call(a,b,c)};var E,F,G,H,fa=function(){return m.navigator?m.navigator.userAgent:null};H=G=F=E=!1;var I;if(I=fa()){var ga=m.navigator;E=0==I.lastIndexOf("Opera",0);F=!E&&(-1!=I.indexOf("MSIE")||-1!=I.indexOf("Trident"));G=!E&&-1!=I.indexOf("WebKit");H=!E&&!G&&!F&&"Gecko"==ga.product}var ha=E,J=F,K=H,L=G,ia=function(){var a=m.document;return a?a.documentMode:void 0},M;
t:{var N="",O;if(ha&&m.opera)var P=m.opera.version,N="function"==typeof P?P():P;else if(K?O=/rv\:([^\);]+)(\)|;)/:J?O=/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/:L&&(O=/WebKit\/(\S+)/),O)var ja=O.exec(fa()),N=ja?ja[1]:"";if(J){var ka=ia();if(ka>parseFloat(N)){M=String(ka);break t}}M=N}
var la=M,ma={},Q=function(a){var b;if(!(b=ma[a])){b=0;for(var c=String(la).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),e=String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),d=Math.max(c.length,e.length),f=0;0==b&&f<d;f++){var g=c[f]||"",h=e[f]||"",v=RegExp("(\\d*)(\\D*)","g"),p=RegExp("(\\d*)(\\D*)","g");do{var l=v.exec(g)||["","",""],C=p.exec(h)||["","",""];if(0==l[0].length&&0==C[0].length)break;b=x(0==l[1].length?0:parseInt(l[1],10),0==C[1].length?0:parseInt(C[1],10))||x(0==l[2].length,
0==C[2].length)||x(l[2],C[2])}while(0==b)}b=ma[a]=0<=b}return b},na=m.document,oa=na&&J?ia()||("CSS1Compat"==na.compatMode?parseInt(la,10):5):void 0;!K&&!J||J&&J&&9<=oa||K&&Q("1.9.1");J&&Q("9");var pa=function(a){a=a.className;return q(a)&&a.match(/\S+/g)||[]},qa=function(a,b){for(var c=pa(a),e=ea(arguments,1),d=c,f=0;f<e.length;f++)0<=B(d,e[f])||d.push(e[f]);c=c.join(" ");a.className=c},sa=function(a,b){var c=pa(a),e=ea(arguments,1),c=ra(c,e).join(" ");a.className=c},ra=function(a,b){return da(a,function(a){return!(0<=B(b,a))})};var R=function(a,b,c){var e=document;c=c||e;var d=a&&"*"!=a?a.toUpperCase():"";if(c.querySelectorAll&&c.querySelector&&(d||b))return c.querySelectorAll(d+(b?"."+b:""));if(b&&c.getElementsByClassName){a=c.getElementsByClassName(b);if(d){c={};for(var f=e=0,g;g=a[f];f++)d==g.nodeName&&(c[e++]=g);c.length=e;return c}return a}a=c.getElementsByTagName(d||"*");if(b){c={};for(f=e=0;g=a[f];f++){var d=g.className,h;if(h="function"==typeof d.split)h=0<=B(d.split(/\s+/),b);h&&(c[e++]=g)}c.length=e;return c}return a};var S=function(a){S[" "](a);return a};S[" "]=function(){};var ta=!J||J&&9<=oa,ua=J&&!Q("9");!L||Q("528");K&&Q("1.9b")||J&&Q("8")||ha&&Q("9.5")||L&&Q("528");K&&!Q("8")||J&&Q("9");var T=function(a,b){this.type=a;this.currentTarget=this.target=b;this.defaultPrevented=this.i=!1};T.prototype.preventDefault=function(){this.defaultPrevented=!0};var U=function(a,b){T.call(this,a?a.type:"");this.relatedTarget=this.currentTarget=this.target=null;this.charCode=this.keyCode=this.button=this.screenY=this.screenX=this.clientY=this.clientX=this.offsetY=this.offsetX=0;this.metaKey=this.shiftKey=this.altKey=this.ctrlKey=!1;this.j=this.state=null;if(a){var c=this.type=a.type;this.target=a.target||a.srcElement;this.currentTarget=b;var e=a.relatedTarget;if(e){if(K){var d;t:{try{S(e.nodeName);d=!0;break t}catch(f){}d=!1}d||(e=null)}}else"mouseover"==
c?e=a.fromElement:"mouseout"==c&&(e=a.toElement);this.relatedTarget=e;this.offsetX=L||void 0!==a.offsetX?a.offsetX:a.layerX;this.offsetY=L||void 0!==a.offsetY?a.offsetY:a.layerY;this.clientX=void 0!==a.clientX?a.clientX:a.pageX;this.clientY=void 0!==a.clientY?a.clientY:a.pageY;this.screenX=a.screenX||0;this.screenY=a.screenY||0;this.button=a.button;this.keyCode=a.keyCode||0;this.charCode=a.charCode||("keypress"==c?a.keyCode:0);this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=a.shiftKey;this.metaKey=
a.metaKey;this.state=a.state;this.j=a;a.defaultPrevented&&this.preventDefault()}};t(U,T);U.prototype.preventDefault=function(){U.n.preventDefault.call(this);var a=this.j;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,ua)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var va="closure_listenable_"+(1E6*Math.random()|0),wa=function(a){try{return!(!a||!a[va])}catch(b){return!1}},xa=0;var ya=function(a,b,c,e,d){this.c=a;this.e=null;this.src=b;this.type=c;this.capture=!!e;this.f=d;this.key=++xa;this.d=this.g=!1},za=function(a){a.d=!0;a.c=null;a.e=null;a.src=null;a.f=null};var V=function(a){this.src=a;this.b={};this.h=0};V.prototype.add=function(a,b,c,e,d){var f=this.b[a];f||(f=this.b[a]=[],this.h++);var g;t:{for(g=0;g<f.length;++g){var h=f[g];if(!h.d&&h.c==b&&h.capture==!!e&&h.f==d)break t}g=-1}-1<g?(a=f[g],c||(a.g=!1)):(a=new ya(b,this.src,a,!!e,d),a.g=c,f.push(a));return a};var Aa=function(a,b){var c=b.type;if(c in a.b){var e=a.b[c],d=B(e,b),f;if(f=0<=d)z(null!=e.length),A.splice.call(e,d,1);f&&(za(b),0==a.b[c].length&&(delete a.b[c],a.h--))}};var W="closure_lm_"+(1E6*Math.random()|0),X={},Ba=0,Da=function(){var a=Ca,b=ta?function(c){return a.call(b.src,b.c,c)}:function(c){c=a.call(b.src,b.c,c);if(!c)return c};return b},Ea=function(a,b,c,e,d){if("array"==n(b))for(var f=0;f<b.length;f++)Ea(a,b[f],c,e,d);else if(c=Fa(c),wa(a))a.k.add(String(b),c,!0,e,d);else{if(!b)throw Error("Invalid event type");var f=!!e,g=Y(a);g||(a[W]=g=new V(a));c=g.add(b,c,!0,e,d);c.e||(e=Da(),c.e=e,e.src=a,e.c=c,a.addEventListener?a.addEventListener(b,e,f):a.attachEvent(b in
X?X[b]:X[b]="on"+b,e),Ba++)}},Ha=function(a,b,c,e){var d=1;if(a=Y(a))if(b=a.b[b])for(b=D(b),a=0;a<b.length;a++){var f=b[a];f&&f.capture==c&&!f.d&&(d&=!1!==Ga(f,e))}return Boolean(d)},Ga=function(a,b){var c=a.c,e=a.f||a.src;if(a.g&&"number"!=typeof a&&a&&!a.d){var d=a.src;if(wa(d))Aa(d.k,a);else{var f=a.type,g=a.e;d.removeEventListener?d.removeEventListener(f,g,a.capture):d.detachEvent&&d.detachEvent(f in X?X[f]:X[f]="on"+f,g);Ba--;(f=Y(d))?(Aa(f,a),0==f.h&&(f.src=null,d[W]=null)):za(a)}}return c.call(e,
b)},Ca=function(a,b){if(a.d)return!0;if(!ta){var c;if(!(c=b))t:{c=["window","event"];for(var e=m,d;d=c.shift();)if(null!=e[d])e=e[d];else{c=null;break t}c=e}d=c;c=new U(d,this);e=!0;if(!(0>d.keyCode||void 0!=d.returnValue)){t:{var f=!1;if(0==d.keyCode)try{d.keyCode=-1;break t}catch(g){f=!0}if(f||void 0==d.returnValue)d.returnValue=!0}d=[];for(f=c.currentTarget;f;f=f.parentNode)d.push(f);for(var f=a.type,h=d.length-1;!c.i&&0<=h;h--)c.currentTarget=d[h],e&=Ha(d[h],f,!0,c);for(h=0;!c.i&&h<d.length;h++)c.currentTarget=
d[h],e&=Ha(d[h],f,!1,c)}return e}return Ga(a,new U(b,this))},Y=function(a){a=a[W];return a instanceof V?a:null},Ia="__closure_events_fn_"+(1E9*Math.random()>>>0),Fa=function(a){z(a,"Listener can not be null.");if("function"==n(a))return a;z(a.handleEvent,"An object listener must have handleEvent method.");return a[Ia]||(a[Ia]=function(b){return a.handleEvent(b)})};var $=function(a,b,c){"number"==typeof a?(this.a=Ja(a,b||0,c||1),Z(this,c||1)):(b=typeof a,"object"==b&&null!=a||"function"==b?(this.a=Ja(a.getFullYear(),a.getMonth(),a.getDate()),Z(this,a.getDate())):(this.a=new Date(aa()),this.a.setHours(0),this.a.setMinutes(0),this.a.setSeconds(0),this.a.setMilliseconds(0)))},Ja=function(a,b,c){b=new Date(a,b,c);0<=a&&100>a&&b.setFullYear(b.getFullYear()-1900);return b};k=$.prototype;k.getFullYear=function(){return this.a.getFullYear()};k.getYear=function(){return this.getFullYear()};
k.getMonth=function(){return this.a.getMonth()};k.getDate=function(){return this.a.getDate()};k.getTime=function(){return this.a.getTime()};k.getUTCHours=function(){return this.a.getUTCHours()};k.setFullYear=function(a){this.a.setFullYear(a)};k.setMonth=function(a){this.a.setMonth(a)};k.setDate=function(a){this.a.setDate(a)};
k.add=function(a){if(a.o||a.m){var b=this.getMonth()+a.m+12*a.o,c=this.getYear()+Math.floor(b/12),b=b%12;0>b&&(b+=12);var e;t:{switch(b){case 1:e=0!=c%4||0==c%100&&0!=c%400?28:29;break t;case 5:case 8:case 10:case 3:e=30;break t}e=31}e=Math.min(e,this.getDate());this.setDate(1);this.setFullYear(c);this.setMonth(b);this.setDate(e)}a.l&&(b=new Date(this.getYear(),this.getMonth(),this.getDate(),12),a=new Date(b.getTime()+864E5*a.l),this.setDate(1),this.setFullYear(a.getFullYear()),this.setMonth(a.getMonth()),
this.setDate(a.getDate()),Z(this,a.getDate()))};k.p=function(){return[this.getFullYear(),w(this.getMonth()+1),w(this.getDate())].join("")+""};k.toString=function(){return this.p()};var Z=function(a,b){if(a.getDate()!=b){var c=a.getDate()<b?1:-1;a.a.setUTCHours(a.a.getUTCHours()+c)}};$.prototype.valueOf=function(){return this.a.valueOf()};new $(0,0,1);new $(9999,11,31);J||L&&Q("525");s("ae.init",function(){Ka();La();Ea(window,"load",function(){});Ma()});
var Ka=function(){var a;a=document;if(a=q("ae-content")?a.getElementById("ae-content"):"ae-content"){a=R("table","ae-table-striped",a);for(var b=0,c;c=a[b];b++){c=R("tbody",null,c);for(var e=0,d;d=c[e];e++){d=R("tr",null,d);for(var f=0,g;g=d[f];f++)f%2&&qa(g,"ae-even")}}}},La=function(){var a=R(null,"ae-noscript",void 0);ca(D(a),function(a){sa(a,"ae-noscript")})},Ma=function(){m._gaq=m._gaq||[];m._gaq.push(function(){m._gaq._createAsyncTracker("UA-3739047-3","ae")._trackPageview()});(function(){var a=
document.createElement("script");a.src=("https:"==document.location.protocol?"https://ssl":"http://www")+".google-analytics.com/ga.js";a.setAttribute("async","true");document.documentElement.firstChild.appendChild(a)})()};s("ae.trackPageView",function(){m._gaq&&m._gaq._getAsyncTracker("ae")._trackPageview()});var Oa=function(a){if(void 0==a||null==a||0==a.length)return 0;a=Math.max.apply(Math,a);return Na(a)},Na=function(a){var b=5;2>b&&(b=2);b-=1;return Math.ceil(a/b)*b},Pa=function(a,b,c){a=a.getSelection();1==a.length&&(a=a[0],null!=a.row&&(null!=b.starttime&&(c+="&starttime="+b.starttime),null!=b.endtime&&(c+="&endtime="+b.endtime),null!=b.latency_lower&&(c+="&latency_lower="+b.latency_lower),null!=b.latency_upper&&(c+="&latency_upper="+b.latency_upper),b=c+"&detail="+a.row,window.location.href=b))},
Qa=function(a,b,c,e,d){var f=new google.visualization.DataTable;f.addColumn("string","");f.addColumn("number","");f.addColumn({type:"string",role:"tooltip"});for(var g=0;g<b.length;g++)f.addRow(["",b[g],c[g]]);c=Math.max(10*b.length,200);b=Oa(b);a=new google.visualization.ColumnChart(document.getElementById("rpctime-"+a));a.draw(f,{height:100,width:c,legend:"none",chartArea:{left:40},fontSize:11,vAxis:{minValue:0,maxValue:b,gridlines:{count:5}}});google.visualization.events.addListener(a,"select",
r(Pa,a,e,d))};s("ae.Charts.latencyHistogram",function(a,b,c){var e=new google.visualization.DataTable;e.addColumn("string","");e.addColumn("number","");for(var d=0;d<b.length;d++)e.addRow([""+a[d],b[d]]);for(d=b.length;d<a.length;d++)e.addRow([""+a[d],0]);b=Oa(b);(new google.visualization.ColumnChart(document.getElementById("latency-"+c))).draw(e,{legend:"none",width:20*a.length,height:200,vAxis:{maxValue:b,gridlines:{count:5}}})});
s("ae.Charts.latencyTimestampScatter",function(a,b,c,e,d){var f=new google.visualization.DataTable;f.addColumn("number","Time (seconds from start)");f.addColumn("number","Latency");for(var g=0;g<a.length;g++){var h=Math.round(a[g]-c);f.addRow([h,b[g]])}a=e.starttime?e.starttime:0;b=new google.visualization.ScatterChart(document.getElementById("LatencyVsTimestamp"));b.draw(f,{hAxis:{title:"Time (seconds from start of recording)",minValue:a},vAxis:{title:"Request Latency (milliseconds)",minValue:0},
tooltip:{trigger:"none"},legend:"none"});google.visualization.events.addListener(b,"select",r(Pa,b,e,d))});
s("ae.Charts.entityCountBarChart",function(a,b,c,e){var d=new google.visualization.DataTable;d.addColumn("string","");d.addColumn("number","Reads");d.addColumn({type:"string",role:"tooltip"});d.addColumn("number","Misses");d.addColumn({type:"string",role:"tooltip"});d.addColumn("number","Writes");d.addColumn({type:"string",role:"tooltip"});var f=50;f>b.length&&(f=b.length);for(var g=0;g<f;g++)d.addRow(["",b[g][1]-b[g][3],b[g][0],b[g][3],b[g][0],b[g][2],b[g][0]]);b=20*f;f=b+130;a=new google.visualization.ColumnChart(document.getElementById(e+
"-"+a));c=Na(c);a.draw(d,{height:100,width:f,chartArea:{width:b},fontSize:10,isStacked:!0,vAxis:{minValue:0,maxValue:c,gridlines:{count:5}}})});
s("ae.Charts.rpcVariationCandlestick",function(a){var b=new google.visualization.DataTable;b.addColumn("string","");b.addColumn("number","");b.addColumn("number","");b.addColumn("number","");b.addColumn("number","");b.addRows(a);(new google.visualization.CandlestickChart(document.getElementById("rpcvariation"))).draw(b,{vAxis:{title:"RPC Latency variation (milliseconds)"},hAxis:{textPosition:"out",slantedText:!0,slantedTextAngle:45,textStyle:{fontSize:13}},height:250,chartArea:{top:10,height:100},
legend:"none",tooltip:{trigger:"none"}})});s("ae.Charts.totalTimeBarChart",function(a,b,c,e){for(var d=[],f=0;f<b.length;f++)d[f]=b[f]+" milliseconds";Qa(a,b,d,c,e)});s("ae.Charts.rpcTimeBarChart",function(a,b,c,e,d){var f=[],g=[],h=c.indices,v=c.times;c=c.stats;for(var p=0;p<b;p++)f[p]=0,g[p]=null;for(p=0;p<h.length;p++){f[h[p]]=v[p];b=c[p];var l="Calls: "+b[0];if(0<b[1]||0<b[2]||0<b[3])l+=" Entities";0<b[1]&&(l+=" R:"+b[1]);0<b[2]&&(l+=" W:"+b[2]);0<b[3]&&(l+=" M:"+b[3]);g[h[p]]=l}Qa(a,f,g,e,d)});})();
