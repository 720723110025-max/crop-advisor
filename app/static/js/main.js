// ===============================
// Sidebar Toggle
// ===============================

function toggleSidebar() {

    const sidebar = document.getElementById("sidebar");

    sidebar.classList.toggle("collapsed");

}

// ===============================
// Dark Mode
// ===============================

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

    } else {

        localStorage.setItem("theme", "light");

    }

}

window.onload = function () {

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");

    }

};

// ===============================
// Auto Close Alerts
// ===============================

setTimeout(function () {

    document.querySelectorAll(".alert").forEach(function (alert) {

        alert.classList.remove("show");

    });

}, 4000);

// ===============================
// Counter Animation
// ===============================

document.querySelectorAll(".counter").forEach(counter => {

    const update = () => {

        const target = +counter.getAttribute("data-target");

        const count = +counter.innerText;

        const increment = Math.ceil(target / 50);

        if (count < target) {

            counter.innerText = count + increment;

            setTimeout(update, 30);

        } else {

            counter.innerText = target;

        }

    };

    update();

});

// ===============================
// Scroll To Top Button
// ===============================

const scrollBtn = document.createElement("button");

scrollBtn.innerHTML = "⬆";

scrollBtn.className = "scroll-top";

document.body.appendChild(scrollBtn);

window.addEventListener("scroll", function () {

    if (window.scrollY > 300) {

        scrollBtn.style.display = "block";

    } else {

        scrollBtn.style.display = "none";

    }

});

scrollBtn.onclick = function () {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

};

// ===============================
// Fade Animation
// ===============================

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll(".fade-card").forEach(card => {

    observer.observe(card);

});

// ===============================
// Loading Spinner
// ===============================

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    if (loader) {

        loader.style.display = "none";

    }

}); 