document.addEventListener("DOMContentLoaded", () => {
  // ================== UP ARROW ==================
  const upArrow = document.querySelector(".up-errow");

  if (upArrow) {
    upArrow.style.display = "none";

    window.addEventListener("scroll", () => {
      if (window.scrollY > 580) {
        upArrow.style.display = "flex";
      } else {
        upArrow.style.display = "none";
      }
    });

    upArrow.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // ================== HEADERS ANIMATION ==================
  const headers = [
    "all-header1",
    "all-header2",
    "all-header3",
    "all-header4",
    "all-header5",
    "all-header6",
    "all-header7",
  ];

  window.addEventListener("scroll", () => {
    headers.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;

      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 10) {
        el.style.transform = "translateY(0)";
      }
    });
  });
});

// feauter-box-4 
document.addEventListener("DOMContentLoaded", () => {
  const boxes = [
    "feature-box1",
    "feature-box2",
    "feature-box3",
    "feature-box4"
  ];

  window.addEventListener("scroll", () => {
    boxes.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;

      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 10) {
        el.style.transform = "translateY(0)";
      }
    });
  });
});

// mission-vision 

document.addEventListener("DOMContentLoaded", () => {
  const sections = [
    "mission-text",
    "vision-text"
  ];

  window.addEventListener("scroll", () => {
    sections.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;

      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 20) {
        el.style.transform = "translateX(0)";
      }
    });
  });
});

// welcome 
document.addEventListener("DOMContentLoaded", () => {
  const sections = [
    "welcome-text-1",
    "welcome-text-2",
  ];

  window.addEventListener("scroll", () => {
    sections.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;

      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 20) {
        el.style.transform = "translateX(0)";
      }
    });
  });
});

// ----mini-slider===
document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("small-slider");

  window.addEventListener("scroll", () => {
    const rect = slider.getBoundingClientRect();

    if (rect.top < window.innerHeight - 50) {
      slider.classList.add("active");
    }
  });
});

// information-tractor-tillage-etc------------
document.addEventListener("DOMContentLoaded", () => {
  const headings = document.querySelectorAll("#information-heading");

  window.addEventListener("scroll", () => {
    headings.forEach(heading => {
      const rect = heading.getBoundingClientRect();

      if (rect.top < window.innerHeight - 10) {
        heading.classList.add("active");
      }
    });
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll('#information-text');

  window.addEventListener("scroll", () => {
    items.forEach(item => {
      const rect = item.getBoundingClientRect();

      if (rect.top < window.innerHeight - 50) {
        item.classList.add("active");
      }
    });
  });
});


// india-map-
document.addEventListener("DOMContentLoaded", () => {
  const elements = [
    document.getElementById("india-map-text-1"),
    document.getElementById("india-map-text-2"),
  ];

  window.addEventListener("scroll", () => {
    elements.forEach(el => {
      if (!el) return;

      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 50) {
        el.classList.add("active");
      }
    });
  });
});



// -------------customer-review----------
document.addEventListener("DOMContentLoaded", () => {
  const reviews = [
    document.getElementById("customer-review-box-1"),
    document.getElementById("customer-review-box-2"),
    document.getElementById("customer-review-box-3"),
  ];

  window.addEventListener("scroll", () => {
    reviews.forEach(box => {
      if (!box) return;

      const rect = box.getBoundingClientRect();
      if (rect.top < window.innerHeight - 30) {
        box.classList.add("active");
      }
    });
  });
});




// =====================loder-all-page-=========================
 window.addEventListener("load", function () {
        const loader = document.getElementById("page-loader");
        if (loader) {
            loader.style.display = "none";
        }
    });


// ================= PAGE LOADER =================
// ================= PAGE LOADER =================
document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("page-loader");
    if (!loader) return;

    // Show loader on link click
    document.querySelectorAll("a[href]").forEach(link => {
        link.addEventListener("click", () => {
            loader.classList.remove("hide");
        });
    });

    // Show loader on form submit
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            loader.classList.remove("hide");
        });
    });
});
// =========================password-validation============================

document.addEventListener("DOMContentLoaded", function () {
  const passwordInput = document.getElementById("password");

  const lengthRule    = document.getElementById("length");
  const uppercaseRule = document.getElementById("uppercase");
  const lowercaseRule = document.getElementById("lowercase");
  const numberRule    = document.getElementById("number");
  const specialRule   = document.getElementById("special");

  passwordInput.addEventListener("input", function () {
    const value = passwordInput.value;

    lengthRule.className    = value.length >= 8        ? "text-green-600" : "text-red-500";
    uppercaseRule.className = /[A-Z]/.test(value)      ? "text-green-600" : "text-red-500";
    lowercaseRule.className = /[a-z]/.test(value)      ? "text-green-600" : "text-red-500";
    numberRule.className    = /\d/.test(value)         ? "text-green-600" : "text-red-500";
    specialRule.className   = /[^A-Za-z0-9]/.test(value) ? "text-green-600" : "text-red-500";
  });
});





// ==================================order-cancellation-========================================
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".countdown").forEach(el => {
        const created = parseInt(el.getAttribute("data-created")) * 1000;
        const orderId = el.getAttribute("data-order");
        const timer = document.getElementById("timer-" + orderId);

        if (!timer || isNaN(created)) return;

        function update() {
            const end = created + (24 * 60 * 60 * 1000);
            const diff = end - Date.now();

            if (diff <= 0) {
                timer.textContent = "Expired";
                el.classList.add("text-gray-400");
                return;
            }

            const h = Math.floor(diff / (1000 * 60 * 60));
            const m = Math.floor((diff / (1000 * 60)) % 60);
            const s = Math.floor((diff / 1000) % 60);

            timer.textContent = `${h}h ${m}m ${s}s`;
        }

        update();
        setInterval(update, 1000);
    });
});

function confirmCancel(orderId) {
    if (confirm("Are you sure you want to cancel this order?")) {
        window.location.href =
            `/order/request-cancel/${orderId}/`;
    }
}



// =============================live=clock========================

function updateTime() {
  const now = new Date();

  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();

  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12 || 12;
  minutes = String(minutes).padStart(2, "0");
  seconds = String(seconds).padStart(2, "0");

  document.getElementById("clock").textContent =
    `${hours}:${minutes}:${seconds} ${ampm}`;
}

updateTime();
setInterval(updateTime, 1000);
