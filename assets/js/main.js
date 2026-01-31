document.addEventListener("DOMContentLoaded", () => {
  const date_calender = document.querySelector("#date_calender");

  if (date_calender) {
    const today = new Date();

    date_calender.textContent = new Intl.DateTimeFormat(
      "fa-IR",
      { dateStyle: "long" }
    ).format(today);
  }
});

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))