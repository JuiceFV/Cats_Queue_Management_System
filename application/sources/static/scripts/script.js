// Creating a connection with server which receives messages to visually updating.
var evtSource = new EventSource("/update");

// When a server will has shutting down it's closing a connection by receiving an error.
evtSource.onerror = function (e) {
	if (e.eventPhase === EventSource.CLOSED)
		evtSource.close();
}

evtSource.onopen = function () {
	console.log("Client joined");
}

// Variable contains:
// 1) hidingTokenInterval - the interval for token hidding (interval means the function "setInterval")
// 2) hidingImageInterval - the interval for token hidding (interval means the function "setInterval")
// 3) redundant_tokens - if number of tokens in a queue is bigger than 64 then the next tokens writes over here. (For representation ofc) 
var hidingTokenInterval;
var hidingImageInterval;
var redundant_tokens = [];

// The crucial function in SSE' iteration
evtSource.onmessage = function(e) {

	// Data from server is fetching as "<server-event-name> <data1> <data2> <data3> ..."
	let fetched_data = e.data.split(' ');

	// First option is when a token has been removed from server this event has to be represented on a client-side.
	if(fetched_data[0] === "update-remove")
		displayQueueRemove();

	// The second option is when a token appended on server and also it should be represented to a user
	else if(fetched_data[0] === "update-append")

		// fetched_data[1] - token
		// fetched_data[2] - its (token's) position
		displayQueueAdd(fetched_data[1], parseInt(fetched_data[2]));

	// The last possible options is that if the web-page will has refreshed a data in redundant_tokens should be rewritten
	else if (fetched_data[0] === "update-redtokens"){

		// in purpose to skip fucking with idexes, we merely removing the "update-redtokens" from array. (Forgive me for my lang:))
		fetched_data.shift();

		// Creating variables for token' wrapping
		let tag;
		let text;

		// Wrapping tokens and store it into the array.
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
	clearInterval(hidingTokenInterval);
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

function autoTokenPartReclaim(delay){
	var print_sec = delay;

	hidingTokenInterval = setInterval(function () {
		$('#timer').html(print_sec + " seconds remain");
		print_sec = print_sec - 1;
		if (print_sec < 5){
			$('#timer').css('color', 'rgb(255, 0,0)');
		}
		if (print_sec < 0){
			if (document.getElementById('show-token-content').style.display === 'flex'){
				returnBack();
			}
		}
	}, 1000);
}

function timerForImageRepresentation(delay){
	var print_sec = delay;

	hidingImageInterval = setInterval(function () {
		$('#seconds-representation-box').html(print_sec + " seconds remain");
		print_sec = print_sec - 1;

		if (print_sec < 5){
			$('#seconds-representation-box').css('color', 'rgb(255, 0,0)');
		}

		if (print_sec < 0){
			returnBackImage();
		}
	}, 1000);
}

function displayQueueAdd(token, token_position){
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

function  displayQueueRemove(){
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

function returnBackImage() {
	$('#check-token').css('display', 'flex');
	$('#image-toolbar').css('display', 'none');
	$('#image').attr('src', "").css('display', 'none');
	clearInterval(hidingImageInterval);
	$('#seconds-representation-box').html("60 seconds remain").css('color', '#333');
	$.get(
		'/start-delay'
	);

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
				autoTokenPartReclaim(14);
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
				$('#check-token').css('display', 'none');
				},
		}).done(function (data) {
			if (data.status === 'success') {
				$('#image').attr('src', data.image_url).css('display', 'flex');
				$('.loader-wrapper').css('display', 'none');
				$('#image-toolbar').css('display', 'flex');
				$('#download-button-box a').attr('href', data.image_url);
				timerForImageRepresentation(60);
			}else if (data.status === 'wrong_turn'){
				$('.loader-wrapper').css('display', 'none');
				alert("It's not your turn");
				returnBackImage();
			}else if (data.status === 'cheater'){
				$('.loader-wrapper').css('display', 'none');
				alert("You're cheater therefore you banned");
				returnBackImage();
			}else if (data.status === 'banned'){
				$('.loader-wrapper').css('display', 'none');
				alert("You were banned");
				returnBackImage();
			}else{
				$('.loader-wrapper').css('display', 'none');
				alert("There are no any tokens");
				returnBackImage();
			}
		});
		event.preventDefault();
	});
})
