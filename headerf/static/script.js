// Navbar toggle for mobile
const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");

menuBtn.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

// Button click animation
const btn = document.querySelector(".btn");
btn.addEventListener("click", () => {
  alert("Welcome to MyWebsite! 🚀");
});
