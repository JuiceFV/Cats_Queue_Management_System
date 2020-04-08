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

	var x = setInterval(function () {
		document.getElementById('timer').innerHTML = print_sec + " seconds remain";
		print_sec = print_sec - 1;
		if (print_sec < 5){
			document.getElementById('timer').style.color = 'rgb(255, 0,0)';
		}
		if (print_sec < 0){
			clearInterval(x);
			if (document.getElementById('show-token-content').style.display === 'flex'){
				returnBack();
				document.getElementById('timer').style.color = '#333';
			}
			document.getElementById('timer').innerHTML = "15 seconds remain";
		}
	}, 1000);
}

$(document).ready(function () {
	$('#get-token-part').on('submit', function (event) {
		$.ajax({
			type: 'get',
			url: '/get-token',
			dataType: 'json'
		}).done(function (data) {
			$('#token-part').hide();
			$('#queue-tablet-part').hide();
			$('#token').text(data.token);
			$('#show-token-content').css('display', 'flex');
			autoReturnBack(14);
		});
		event.preventDefault();
	});

	$('#check-token').on('submit', function (event) {
		$.ajax({
			type: 'post',
			url: '/post-token',
			data: $('input').serialize(),
			dataType: 'json'
		}).done(function (data) {
			if (data.status === 'success') {
				$('#image').attr('src', data.image_url);
				$('#image-box').css('display', 'flex');
			}else if (data.status === 'wrong_turn'){
				alert("It's not your turn");
			}else if (data.status === 'cheater'){
				alert("Cheating");
			}else{
				alert("There are no any tokens");
			}
		});
		event.preventDefault();
	});
})