
SyntaxHighlighter.all();

tinyMCE.init({
	        // General options
	        mode : "textareas",
	        theme : "advanced",
	        plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,syntaxhl",
	
	        // Theme options
	        theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
	        theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,syntaxhl,|,insertdate,inserttime,preview,|,spellchecker",
	        theme_advanced_toolbar_location : "top",
	        theme_advanced_toolbar_align : "left",
	        theme_advanced_statusbar_location : "bottom",
	        theme_advanced_resizing : true,
	
			extended_valid_elements : "pre[name|class]",
	
	        // Skin options
	        skin : "o2k7",
	        skin_variant : "silver",
	
	        // Example content CSS (should be your site CSS)
//	        content_css : "/static/css/public_base.css",
	
	        // Drop lists for link/image/media/template dialogs
	        external_link_list_url : "js/link_list.js",
	        external_image_list_url : "js/image_list.js",
	        media_external_list_url : "js/media_list.js",
			relative_urls : false,	        
});
