document.addEventListener("DOMContentLoaded", () => {
  const date_calender = document.querySelector("#date_calender");

  if (date_calender) {
    const today = new Date();

    date_calender.textContent = new Intl.DateTimeFormat("fa-IR", {
      dateStyle: "medium",
    }).format(today);
  }
});

const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]',
);
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl),
);

window.addEventListener("load", function () {
  document.getElementById("loading-screen").style.display = "none";
  document.getElementById("main-content").style.display = "block";
});


document.addEventListener("DOMContentLoaded", function () {
  const toastElList = document.querySelectorAll('.toast')
  toastElList.forEach(function (toastEl) {
    const toast = new bootstrap.Toast(toastEl)
    toast.show()
  })
})