function showForm() {
    let hidden = document.getElementsByClassName("hide");
    let shown = document.getElementsByClassName("show");
    let inputs = document.getElementsByTagName("input");

    for (item of shown) {
        item.style.display = "none";
    }

    for (item of hidden) {
        item.style.display = "inline";
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
        element.children[1].value--;
        prev.children[1].value++;
    }
}

function moveToTop(button) {
    let element = button.parentNode.parentNode;
    let list = element.parentNode;
    let prev = element.previousElementSibling;

    while (prev) {
        list.insertBefore(element, prev);
        prev.children[1].value++;
        prev = element.previousElementSibling;
    }

    element.children[1].value = 1;
}

function moveDown(button) {
    let element = button.parentNode.parentNode;
    let list = element.parentNode;
    let next = element.nextElementSibling;

    if (next) {
        list.insertBefore(next, element);
        element.children[1].value++;
        next.children[1].value--;
    }
}

function moveToBottom(button) {
    let element = button.parentNode.parentNode;
    let list = element.parentNode;
    let next = element.nextElementSibling;

    while (next) {
        list.insertBefore(next, element);
        next.children[1].value--;
        next = element.nextElementSibling;
    }

    element.children[1].value = list.childElementCount;
}

function confirmDeletion() {
    return prompt('Scrivi "Sì, sono sicuro" per cancellare la lista') == "Sì, sono sicuro";
}
