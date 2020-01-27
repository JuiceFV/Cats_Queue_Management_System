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