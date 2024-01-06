const inputText = document.getElementById("input-text"),
    inputFile = document.getElementById("input-file"),
    textRadio = document.getElementById("text-radio"),
    button = document.querySelector('button[type="submit"]'),
    loadingIcon = document.getElementById("loader"),
    loadingContainer = document.getElementById("loader-cotainer");



window.onload = function () {
    toggleForm();
    loadingIcon.classList.add("delete");
    loadingContainer.classList.add("delete");
};

function toggleForm() {
    if (textRadio.checked) {
        inputFile.classList.add("delete");
        inputText.classList.remove("delete");
    } else {
        inputText.classList.add("delete");
        inputFile.classList.remove("delete");
    }
}

function disableButton() {
    loadingIcon.classList.remove("delete");
    loadingContainer.classList.remove("delete");
}
