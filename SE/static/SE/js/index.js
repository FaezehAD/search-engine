const form = document.querySelector("form"),
  searchInput = document.getElementById("query"),
  errorContainer = document.getElementById("error-container");

form.addEventListener("submit", function (event) {
  event.preventDefault();
  if (searchInput.value.trim() === "") {
    errorContainer.classList.add("show");
  } else {
    errorContainer.classList.remove("show");
    form.submit();
  }
});

searchInput.addEventListener("input", () => {
  errorContainer.classList.remove("show");
});
