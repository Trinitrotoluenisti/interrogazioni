function showForm() {
    let hidden = document.getElementsByClassName("hide");
    let shown = document.getElementsByClassName("show");
    let inputs = document.getElementsByTagName("input");

    for (item of shown) {
        item.style.visibility = "hidden";
    }

    for (item of hidden) {
        item.style.visibility = "visible";
    }

    for (input of inputs) {
        if (input.type == "checkbox") {
            input.disabled = false;
        }
    }
}

function moveUp(button) {
    let element = button.parentNode.parentNode;
    let list = element.parentNode;
    let prev = element.previousElementSibling;

    if (prev) {
        list.insertBefore(element, prev);
        element.children[2].value--;
        prev.children[2].value++;
    }
}

function moveDown(button) {
    let element = button.parentNode.parentNode;
    let list = element.parentNode;
    let next = element.nextElementSibling;

    if (next) {
        list.insertBefore(next, element);
        element.children[2].value++;
        next.children[2].value--;
    }
}

function confirmDeletion() {
    return prompt('Scrivi "Sì, sono sicuro" per cancellare la lista') == "Sì, sono sicuro";
}
