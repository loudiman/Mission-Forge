    const nav = document.querySelector(".nav");
    const menuButton = document.querySelector(".mobile-menu-button");
    const mobilePanel = document.querySelector("#mobile-panel");
    const terminalLines = [...document.querySelectorAll(".terminal-line")];
    const highlightRow = document.querySelector("#benchmark-highlight");
    const placeholders = [...document.querySelectorAll(".placeholder")];

    function syncNavShadow() {
      nav.classList.toggle("scrolled", window.scrollY > 40);
    }

    function toggleMenu(force) {
      const open = typeof force === "boolean" ? force : !mobilePanel.classList.contains("open");
      mobilePanel.classList.toggle("open", open);
      menuButton.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("menu-open", open);
    }

    menuButton.addEventListener("click", () => toggleMenu());
    document.querySelectorAll(".mobile-panel a").forEach((link) => {
      link.addEventListener("click", () => toggleMenu(false));
    });

    window.addEventListener("scroll", syncNavShadow, { passive: true });
    syncNavShadow();

    terminalLines.forEach((line, index) => {
      window.setTimeout(() => line.classList.add("visible"), 220 + index * 150);
    });

    if (window.IntersectionObserver && highlightRow) {
      const rowObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            highlightRow.classList.add("in-view");
            rowObserver.disconnect();
          }
        });
      }, { threshold: 0.45 });

      rowObserver.observe(highlightRow);
    } else if (highlightRow) {
      highlightRow.classList.add("in-view");
    }

    placeholders.forEach((placeholder) => {
      const input = placeholder.querySelector("input[type='file']");
      input.addEventListener("change", () => {
        const [file] = input.files || [];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          placeholder.classList.add("loaded");
          placeholder.innerHTML = "<span class=\"placeholder-meta\">Uploaded preview</span><img alt=\"Uploaded preview\">";
          placeholder.querySelector("img").src = reader.result;
        };
        reader.readAsDataURL(file);
      });
    });
