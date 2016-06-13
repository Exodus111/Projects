$(document).ready(function () {
	// menu
		$("#subCSS").align({topIsBottomOf:'mainMenu', right:"content", left:"CSS"});
		$("#subLayout").align({topIsBottomOf:'mainMenu', right:"content", left:"Layout"});
		$("#subUI").align({topIsBottomOf:'mainMenu', right:"content", left:"UI"});
		
		$("#pink").draggable({ refreshPositions: true });
		$("#pink").bind( "drag", function(event, ui) {$(window).resize();});
		
		//You wouldn't even dreamed of such an easy Layout Manager :) 
		$("#blue").align({leftIsRightOf:'pink', bottomIsTopOf:"pink"});
		$("#blue").limit({top:'container', leftIsRightOf:"orange", bottomIsTopOf:"yellow", right:"container"});
		
		$("#red").align({topIsBottomOf:'blue', leftIsRightOf:"blue"});	//"" is for window
		$("#red").limit({right:'container', bottom: 'container'});	
		
		$("#yellow").align({topIsBottomOf:'red', leftIsRightOf:"red"});
		$("#yellow").limit({bottom: 'container', right:"container"});
		
		$("#orange").align({top:'container', bottom:"container", left:"container", rightIsLeftOf:'pink'});
		$("#orange").limit({rightIsLeftOf:'blue'});
		$("#Layout").setSubMenu({
			id: "subLayout", 
			openFunction : function(me) {
				$('.play').removeClass("hidden");
				me.removeClass("hidden");
				$(window).resize();
			}, 
			closeFunction : function(me) {
				$('.play').addClass("hidden");
				me.addClass("hidden");
			}
			
			
		});
			
		//easy create submenus 
		$("#CSS").setSubMenu('subCSS');
		$("#UI").setSubMenu('subUI');
}); 