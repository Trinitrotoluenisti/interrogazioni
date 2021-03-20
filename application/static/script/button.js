let buttonClicked = false;
let hidden = document.getElementsByClassName("hide");
let shown = document.getElementsByClassName("show");

function buttonClick() {
    if (!buttonClicked) {
        for (item of shown) {
            item.style.visibility = "hidden";
        }

        for (item of hidden) {
            item.style.visibility = "visible";
        }
    } else {
        for (item of hidden) {
            item.style.visibility = "hidden";
        }

        for (item of shown) {
            item.style.visibility = "visible";
        }
    }

    buttonClicked = !buttonClicked;
}