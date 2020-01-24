// $(document).ready(function(){
// 	$('.left-sidebar').mouseover(function(){
// 		$('.right-sidebar').css('margin-right', '2%');
// 		$(this).css('width', '50%');
// 	});
// 	$('.left-sidebar').mouseout(function(){
// 		$('.right-sidebar').css('margin-right', '0');
// 		$(this).css('width', '44%');
// 	});
// 	$('.right-sidebar').mouseover(function(){
// 		$('.left-sidebar').css('margin-left', '2%');
// 		$(this).css('width', '50%');
// 	});
// 	$('.right-sidebar').mouseout(function(){
// 		$('.left-sidebar').css('margin-left', '0');
// 		$(this).css('width', '44%');
// 	});
// });

// function which defies the behavior when the mouse cursor is within of the div block
function activeSidebar(active, unactive){
	var activePart = document.getElementsByClassName(active + '-sidebar')[0];
	var unactivePart = document.getElementsByClassName(unactive + '-sidebar')[0];
	activePart.style.width = "50%";
	activePart.style.boxShadow = "0 0 25px rgba(0,0,0,0.5)";
	activePart.style.borderRadius = "12px"
}

// function which defies the behavior when the mouse cursor is out of the div block
function unactiveSidebar(active, unactive){
	var activePart = document.getElementsByClassName(active + '-sidebar')[0];
	var unactivePart = document.getElementsByClassName(unactive + '-sidebar')[0];
	activePart.style.width = "44%";
	activePart.style.boxShadow = "none";
}

function getTokentInterfaceClick(){
 	var getBtn = document.getElementsByClassName('get-token-button')[0];
	var interface = document.getElementsByClassName('get-token-interface')[0];
	var queue = document.getElementsByClassName('queue')[0];
	queue.style.display = "none";
	getBtn.style.display = "none";
	interface.style.display = "inline";
}
function tokenInterfaceNoButton(){
 	var getBtn = document.getElementsByClassName('get-token-button')[0];
	var interface = document.getElementsByClassName('get-token-interface')[0];
	var queue = document.getElementsByClassName('queue')[0];
	queue.style.display = "block";
	getBtn.style.display = "block";
	interface.style.display = "none";
}
function tokenInterfaceYesButton(){
	var getBtn = document.getElementsByClassName('get-token-button')[0];
	var interface = document.getElementsByClassName('show-token-interface')[0];
	var btnInterface = document.getElementsByClassName('get-token-interface')[0];
	btnInterface.style.display = "none";
	getBtn.style.display = "none";
	interface.style.display = "block";
}
function copyButton(){
	var range = document.createRange();
	range.selectNode(document.getElementById("token"));
	window.getSelection().removeAllRanges(); // clear current selection
	window.getSelection().addRange(range); // to select text
	document.execCommand("copy");
	window.getSelection().removeAllRanges();// to deselect
}
function backToMenu(){
	var getBtn = document.getElementsByClassName('get-token-button')[0];
	var interface = document.getElementsByClassName('show-token-interface')[0];
	var queue = document.getElementsByClassName('queue')[0];
	queue.style.display = "block";
	getBtn.style.display = "block";
	interface.style.display = "none";
}