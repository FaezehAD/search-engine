const yearContainer = document.getElementById("year-error"),
  yearErrorContent = document.getElementById("year-error-content"),
  startYear = document.getElementById("start-year"),
  endYear = document.getElementById("end-year"),
  andOrContainer = document.querySelector("article"),
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
  keywordsCheckbox = document.getElementById("keywords-checkbox"),
  abstractCheckbox = document.getElementById("abstracts-checkbox"),
  bodiesCheckbox = document.getElementById("bodies-checkbox"),
  serialContainer = document.getElementById("serial-container"),
  selectElement = document.getElementById("options");


function disableCheckboxes() {
  var selectedValue = selectElement.value;
  if (selectedValue == 'article') {
    if (semanticRadio.checked) {
      keywordsCheckbox.checked = false;
      abstractCheckbox.checked = false;
      bodiesCheckbox.checked = false;
      keywordsCheckbox.disabled = true;
      abstractCheckbox.disabled = true;
      bodiesCheckbox.disabled = true;
    } else {
      bodiesCheckbox.checked = false;
      bodiesCheckbox.disabled = true;
    }
  }
  else {
    keywordsCheckbox.disabled = false;
    abstractCheckbox.disabled = false;
    bodiesCheckbox.disabled = false;
  }
}

function handleSelectChange() {
  var selectedValue = selectElement.value;
  if (selectedValue == 'report') {
    if (serialContainer.classList.contains("delete")) {
      serialContainer.classList.remove("delete");
    }
  } else if (selectedValue == 'article') {
    if (!serialContainer.classList.contains("delete")) {
      serialContainer.classList.add("delete");
    }
  }
  disableCheckboxes();
}

selectElement.addEventListener("change", handleSelectChange);

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
    andOrContainer.classList.add("delete");
    // bodiesCheckbox.disabled = true;
    // bodiesCheckbox.checked = false;
  } else {
    andOrContainer.classList.remove("delete");
    // bodiesCheckbox.disabled = false;
  }
  disableCheckboxes();
}

function addPerson() {
  if (people2.classList.contains("delete")) {
    people2.classList.remove("delete");
  } else if (people3.classList.contains("delete")) {
    people3.classList.remove("delete");
    plusContainer.classList.add("delete");
  }
}

window.addEventListener("load", function () {
  toggleSearch();
  handleSelectChange();
});
