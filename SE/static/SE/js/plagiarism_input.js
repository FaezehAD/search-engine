const inputText = document.getElementById("input-text"),
    inputFile = document.getElementById("input-file"),
    textRadio = document.getElementById("text-radio");

window.onload = function () {
    toggleForm();
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
