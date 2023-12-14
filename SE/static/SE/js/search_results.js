const resultsContainer = document.getElementById("results-filtered"),
  dateRadio = document.getElementById("date"),
  ascendingRadio = document.getElementById("ascending"),
  departmentCheckboxes = document.querySelectorAll('input[name="department"]'),
  query = document.querySelector("[name=query]"),
  resultsFiltered = document.getElementById("results-filtered"),
  loadingIcon = document.getElementById("loader"),
  loadingContainer = document.getElementById("loader-cotainer"),
  correct_normal = document.querySelectorAll(".correct_normal"),
  incorrect_normal = document.querySelectorAll(".incorrect_normal"),
  queryIdContainer = document.getElementById("query-id");

for (let i = 0; i < correct_normal.length; i++) {
  correct_normal[i].addEventListener("click", function (event) {
    feedbackClicked(event, true);
  });
}

for (let i = 0; i < incorrect_normal.length; i++) {
  incorrect_normal[i].addEventListener("click", function (event) {
    feedbackClicked(event, false);
  });

}

var date_checked = 0;
var ascending_checked = 0;

window.addEventListener("load", function () {
  loadingIcon.classList.add("delete");
  loadingContainer.classList.add("delete");
});


function updateSearchResults() {

  loadingIcon.classList.remove("delete");
  loadingContainer.classList.remove("delete");
  const selectedDepartments = Array.from(departmentCheckboxes)
    .filter((checkbox) => checkbox.checked)
    .map((checkbox) => checkbox.value);
  if (dateRadio.checked) {
    date_checked = 1;
  } else {
    date_checked = 0;
  }
  if (ascendingRadio.checked) {
    ascending_checked = 1;
  } else {
    ascending_checked = 0;
  }

  let data = {
    departments: selectedDepartments,
    date: date_checked,
    ascending: ascending_checked,
    query: query.value,
  };

  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/search-engine/search", true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        loadingIcon.classList.add("delete");
        loadingContainer.classList.add("delete");
        resultsFiltered.innerHTML = xhr.responseText;
      } else {
        console.error("Error:", xhr.status);
      }
    }
  };
  xhr.send(JSON.stringify(data));

}


function feedbackClicked(event, isCorrect) {

  const parent = event.target.parentNode;
  var query_id = queryIdContainer.dataset.myparam;

  console.log(query_id)

  var data = {
    result_id: parent.id,
    is_correct: isCorrect,
    query_id: query_id,
  };


  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/search-engine/search", true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
      } else {
        console.error("Error:", xhr.status);
      }
    }
  };
  xhr.send(JSON.stringify(data));


  const children = parent.childNodes;

  for (const child of children) {
    if (child.classList) {
      if (isCorrect) {
        if (child.classList.contains("correct_filled") && child.classList.contains("not-visible")) {

          child.classList.remove("not-visible");

        } else if (child.classList.contains("incorrect_normal") && child.classList.contains("not-visible")) {

          child.classList.remove("not-visible");

        } else if (child.classList.contains("incorrect_filled")) {
          if (!child.classList.contains("not-visible")) {

            child.classList.add("not-visible");

          }
        }
      }
      else { //incorrect
        if (child.classList.contains("correct_filled")) {
          if (!child.classList.contains("not-visible")) {

            child.classList.add("not-visible");

          }
        } else if (child.classList.contains("correct_normal") && child.classList.contains("not-visible")) {

          child.classList.remove("not-visible");

        } else if (child.classList.contains("incorrect_filled") && child.classList.contains("not-visible")) {

          child.classList.remove("not-visible");

        }
      }
    }
  }

  event.target.classList.add("not-visible"); // normal icon

}


function resultClicked(element) {
  var result_id = element.getAttribute("id");
  var query_id = queryIdContainer.dataset.myparam;
  var data = {
    result_id: result_id,
    query_id: query_id,
  };

  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/search-engine/search", true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
      } else {
        console.error("Error:", xhr.status);
      }
    }
  };
  xhr.send(JSON.stringify(data));

}