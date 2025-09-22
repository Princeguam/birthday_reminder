// Basic JavaScript for modal functionality
const addBtn = document.getElementById("addBirthdayBtn");
const modal = document.getElementById("birthdayModal");
const closeBtn = document.getElementById("closeModal");
const form = document.getElementById("birthdayForm");

addBtn.addEventListener("click", () => {
modal.classList.add("show");
});

closeBtn.addEventListener("click", () => {
modal.classList.remove("show");
});

form.addEventListener("submit", async function (e)  {
e.preventDefault();
// Add your form submission logic here
    const birthdayForm = new FormData(form);
    

    try{
        const response = await fetch("http://127.0.0.1:5000/submit",{
        method: "POST",
        body:  birthdayForm
        });

        const result = await response.json();
        console.log("Server Response:", result);

        alert("Birthday submitted Successfully!");

    modal.classList.remove("show");
    } catch(error){
    console.error("Error submitting form", error);
}
});