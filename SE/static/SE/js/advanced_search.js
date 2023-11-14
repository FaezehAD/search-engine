const optionMenu = document.querySelector(".select-menu"),
  yearContainer = document.getElementById("year-error"),
  yearErrorContent = document.getElementById("year-error-content"),
  startYear = document.getElementById("start-year"),
  endYear = document.getElementById("end-year"),
  article = document.querySelector("article"),
  semanticRadio = document.getElementById("semantic-radio"),
  form = document.querySelector("form"),
  searchInput = document.getElementById("query"),
  andInput = document.getElementById("and"),
  orInput = document.getElementById("or"),
  notInput = document.getElementById("not"),
  exactInput = document.getElementById("exact"),
  serialInput = document.getElementById("serial"),
  alertContainer = document.getElementById("alert-container"),
  people1 = document.getElementById("people-1"),
  people2 = document.getElementById("people-2"),
  people3 = document.getElementById("people-3"),
  plusContainer = document.getElementById("plus-container"),
  bodiesCheckbox = document.getElementById("bodies-checkbox");

function closeAlert() {
  alertContainer.classList.add("delete");
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  let status = true
  if (
    searchInput.value == "" &&
    andInput.value == "" &&
    orInput.value == "" &&
    notInput.value == "" &&
    exactInput.value == "" &&
    serialInput.value == "" &&
    people1.value == "" &&
    people2.value == "" &&
    people3.value == ""
  ) {
    alertContainer.classList.remove("delete");
    status = false;
  }
  if (startYear.value != "") {
    var startYearNum = parseInt(startYear.value);
    if (startYearNum < 1) {
      yearErrorContent.textContent = "سال نشر باید مثبت باشد!"
      yearContainer.classList.add("show");
      status = false
    }
  }
  if (endYear.value != "") {
    var endYearNum = parseInt(endYear.value);
    if (endYearNum < 1) {
      yearErrorContent.textContent = "سال نشر باید مثبت باشد!"
      yearContainer.classList.add("show");
      status = false
    }
  }
  if (startYear.value != "" && endYear.value != "") {
    var startYearNum = parseInt(startYear.value);
    var endYearNum = parseInt(endYear.value);
    if (startYearNum > endYearNum) {
      yearContainer.classList.add("show");
      yearErrorContent.textContent = "انتهای محدوده باید بزرگتر از ابتدای محدوده باشد!"
      status = false;
    }
  }

  if (status) {
    yearContainer.classList.remove("show");
    form.submit();
  }

});

function toggleSearch() {
  if (semanticRadio.checked) {
    article.classList.add("delete");
    // bodiesCheckbox.disabled = true;
    // bodiesCheckbox.checked = false;
  } else {
    article.classList.remove("delete");
    // bodiesCheckbox.disabled = false;
  }
}

window.addEventListener("load", toggleSearch);

function addPerson() {
  if (people2.classList.contains("delete")) {
    people2.classList.remove("delete");
  } else if (people3.classList.contains("delete")) {
    people3.classList.remove("delete");
    plusContainer.classList.add("delete");
  }
}
