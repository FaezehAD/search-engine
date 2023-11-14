const form = document.querySelector("form"),
    alertContent = document.getElementById("alert-content"),
    threshold = document.getElementById("threshold");


form.addEventListener("submit", function (event) {
    event.preventDefault();
    let thresholdVal = threshold.value
    let thresholdInt = parseInt(thresholdVal)
    if (thresholdInt != thresholdVal) {
        alertContent.textContent = "حد آستانه باید عدد صحیح باشد!"
    } else if (thresholdVal > 100 || thresholdVal < 1) {
        alertContent.textContent = "حد آستانه باید بین 1 تا 100 باشد!"
    }
    else {
        alertContent.textContent = ""
        form.submit();
    }

});  
