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
  // وقتی کل صفحه و منابع لود شدند
  document.getElementById("loading-screen").style.display = "none";
  document.getElementById("main-content").style.display = "block";
});