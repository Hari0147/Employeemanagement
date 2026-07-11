console.log("Employee Management System Loaded");

// Highlight the selected row
const rows = document.querySelectorAll("table tbody tr");

rows.forEach(row => {

    row.addEventListener("click", () => {

        rows.forEach(r => r.style.backgroundColor = "");

        row.style.backgroundColor = "#d9edf7";

    });

});
