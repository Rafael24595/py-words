function scrollToLast(id, position) {
    cluesElement = document.getElementsByClassName(id);
    position = position == undefined ? cluesElement.length - 1 : position;
    cluesElement[position].scrollIntoView();
}

function click(id) {
    document.getElementById(id).click();
}