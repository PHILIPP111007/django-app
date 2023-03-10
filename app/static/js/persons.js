function backgroundColorChange() {
	var color = window.getComputedStyle(document.body, null).getPropertyValue('background-color');

	if (color === "rgb(250, 244, 244)") {
		document.body.style.backgroundColor = "rgb(220, 244, 244)"
	} else if (color === "rgb(220, 244, 244)") {
		document.body.style.backgroundColor = "rgb(250, 244, 244)"
	}
}

var navButton = document.querySelector('nav button');
navButton.addEventListener('click', function() {
    let expanded = this.getAttribute('aria-expanded') === 'true' || false;
    this.setAttribute('aria-expanded', !expanded);
    let menu = this.nextElementSibling;
    menu.hidden = !menu.hidden;
});