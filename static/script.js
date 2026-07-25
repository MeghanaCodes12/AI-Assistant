document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("mainForm");
    const button = document.getElementById("generateBtn");
    const loading = document.getElementById("loading");

    if (button) {
        button.disabled = false;
        button.innerHTML = "🚀 Generate AI Response";
    }

    if (loading) {
        loading.style.display = "none";
    }

    if (form) {
        form.addEventListener("submit", function () {

            if (loading) {
                loading.style.display = "block";
            }

            if (button) {
                button.disabled = true;
                button.innerHTML = " ⏳ Generating...";
            }

        });
    }

});

function copyResponse() {

    const response = document.getElementById("aiResponse");

    if (!response) return;

    navigator.clipboard.writeText(response.innerText);

    const button = document.getElementById("copyBtn");

    button.innerHTML = "✅ Copied!";

    setTimeout(() => {
        button.innerHTML = "📋 Copy Response";
    }, 2000);

}

const button = document.getElementById("themeToggle");

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}

button.addEventListener("click", function(){
    document.body.classList.toggle("dark");
    if (document.body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        button.innerHTML = "☀️ Light Mode";
    }
    else {
        localStorage.setItem("theme", "light");
        button.innerHTML = "🌙 Dark Mode";
    }
});
