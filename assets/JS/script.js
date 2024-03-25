
function fetchAndInsertCustomerPage() {
  fetch("htmlDict.json") 
    .then((response) => response.json()) 
    .then((data) => {
      const contentElement = document.getElementById("content");
      contentElement.innerHTML = data.customer_page;
    })
    .catch((error) => {
      console.error("Error fetching the JSON:", error);
    });
}
document.addEventListener("DOMContentLoaded", fetchAndInsertCustomerPage);
