const evtSource = new EventSource("/update");

evtSource.onerror = function(e){
	if (e.eventPhase === EventSource.CLOSED){
		evtSource.close();
	}
}

var x;
var redundant_tokens = [];

evtSource.onmessage = function(e) {
	let fetched_data = e.data.split(' ');
	if(fetched_data[0] === "update-remove")
		display_queue_remove();
	else if(fetched_data[0] === "update-append")
		display_queue_add(fetched_data[1], parseInt(fetched_data[2]));
	else if (fetched_data[0] === "update-redtokens"){
		fetched_data.shift();
		let tag;
		let text;
		for(let i = 0; i < fetched_data.length - 1; i++) {
			tag = document.createElement("div");
			text = document.createTextNode(fetched_data[i]);
			tag.appendChild(text);
			tag.setAttribute("class", "token-field");
			redundant_tokens[i] = tag;
		}
	}
}

//A function that makes it seem as if the card is being ejected
function activatePart(part){
	var activePart = document.getElementById(part + '-part');
	activePart.style.width = "50%";
	activePart.style.height = "96%";
	activePart.style.boxShadow = "0 0 25px rgba(0,0,0,0.5)";
	activePart.style.borderRadius = "12px"
}
//A function that makes it seem as if the card is being reclaimed
function disactivatePart(part){
	var activePart = document.getElementById(part + '-part');
	activePart.style.width = "44%";
	activePart.style.height = "90%";
	activePart.style.boxShadow = "none";
}

function returnBack(){
	var tokenPart = document.getElementById('token-part');
	var queuePart = document.getElementById('queue-tablet-part');
	var showTokenContent = document.getElementById('show-token-content');
	tokenPart.style.display = "flex";
	queuePart.style.display = "flex";
	showTokenContent.style.display = "none";
	clearInterval(x);
	document.getElementById('timer').style.color = '#333';
	document.getElementById('timer').innerHTML = "15 seconds remain";
}

function copyButton(){
	var range = document.createRange();
	range.selectNode(document.getElementById("token"));
	window.getSelection().removeAllRanges(); // clear current selection
	window.getSelection().addRange(range); // to select text
	try {
		return document.execCommand("copy");
	}
	catch (ex){
		console.warn("Copy to clipboard failed.", ex);
        return false;
	}
	finally {
		window.getSelection().removeAllRanges();// to deselect
		returnBack();
	}
}

function autoReturnBack(delay){
	var print_sec = delay;

	x = setInterval(function () {
		document.getElementById('timer').innerHTML = print_sec + " seconds remain";
		print_sec = print_sec - 1;
		if (print_sec < 5){
			document.getElementById('timer').style.color = 'rgb(255, 0,0)';
		}
		if (print_sec < 0){
			if (document.getElementById('show-token-content').style.display === 'flex'){
				returnBack();
			}
		}
	}, 1000);
}

function display_queue_add(token, token_position){
	var column;
	var tag = document.createElement("div");
	var text = document.createTextNode(token);
	tag.appendChild(text);
	tag.setAttribute("class", "token-field");
		// cond where res list ! empty
	if (token_position <= 16){
		column = document.getElementById("first-column");
		column.appendChild(tag);
		//adding to the 1st column
	} else if (token_position <= 32) {
		column = document.getElementById("second-column");
		column.appendChild(tag);
	} else if (token_position <= 48) {
		column = document.getElementById("third-column");
		column.appendChild(tag);
	} else if (token_position <= 64) {
		column = document.getElementById("forth-column");
		column.appendChild(tag);
	} else {
		redundant_tokens.push(tag);
	}
}

function  display_queue_remove(){
	var tag;
	var first_column = document.getElementById("first-column");
	var second_column = document.getElementById("second-column");
	var third_column = document.getElementById("third-column");
	var forth_column = document.getElementById("forth-column");
	first_column.removeChild(first_column.firstElementChild);
	if (second_column.firstElementChild){
		tag = second_column.firstElementChild;
		second_column.removeChild(second_column.firstElementChild);
		first_column.appendChild(tag);
	}
	if (third_column.firstElementChild){
		tag = third_column.firstElementChild;
		third_column.removeChild(third_column.firstElementChild);
		second_column.appendChild(tag);
	}
	if (forth_column.firstElementChild){
		tag = forth_column.firstElementChild;
		forth_column.removeChild(forth_column.firstElementChild);
		third_column.appendChild(tag);
	}
	if (redundant_tokens.length > 0) {
		forth_column.appendChild(redundant_tokens.shift());
	}
}


$(document).ready(function () {
	$('#get-token-part').on('submit', function (event) {
		$.ajax({
			type: 'get',
			url: '/get-token',
			dataType: 'json'
		}).done(function (data) {
			if (data.status === "ok") {
				$('#token-part').hide();
				$('#queue-tablet-part').hide();
				$('#token').text(data.token);
				$('#show-token-content').css('display', 'flex');
				autoReturnBack(14);
			} else {
				alert("You were banned");
			}
		});
		event.preventDefault();
	});

	$('#check-token').on('submit', function (event) {
		$.ajax({
			type: 'post',
			url: '/post-token',
			data: $('input').serialize(),
			dataType: 'json',
			beforeSend: function() {
				$('.loader-wrapper').css('display', 'block');
				$('#image').attr('src', "").css('display', 'none');
				},
		}).done(function (data) {
			if (data.status === 'success') {
				$('#image').attr('src', data.image_url).css('display', 'flex');
				$('.loader-wrapper').css('display', 'none');
			}else if (data.status === 'wrong_turn'){
				$('.loader-wrapper').css('display', 'none');
				alert("It's not your turn");
			}else if (data.status === 'cheater'){
				$('.loader-wrapper').css('display', 'none');
				alert("You're cheater therefore you banned");
			}else if (data.status === 'banned'){
				$('.loader-wrapper').css('display', 'none');
				alert("You were banned");
			}else{
				$('.loader-wrapper').css('display', 'none');
				alert("There are no any tokens");
			}
		});
		event.preventDefault();
	});
})
