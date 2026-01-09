// Function to stylize the many flash types
function stylizeFlashMessages() {
  const flashUl = document.querySelector("ul.flashes");
  if (!flashUl) return;

  const styles = {
    success: {
      backgroundColor: "#d4edda",
      border: "1px solid #c3e6cb",
      color: "#155724",
      padding: "10px",
      borderRadius: "8px",
      marginBottom: "10px",
      zIndex: "2",
    },
    danger: {
      backgroundColor: "#f8d7da",
      border: "1px solid #f5c6cb",
      color: "#721c24",
      padding: "10px",
      borderRadius: "8px",
      marginBottom: "10px",
      zIndex: "2",
    },
    warning: {
      backgroundColor: "#fff3cd",
      border: "1px solid #ffeeba",
      color: "#856404",
      padding: "10px",
      borderRadius: "8px",
      marginBottom: "10px",
      zIndex: "2",
    },
  };

  const lis = flashUl.querySelectorAll("li");
  lis.forEach((li) => {
    const category = li.className.trim();
    if (styles[category]) {
      Object.assign(li.style, styles[category]);
    }
  });

  flashUl.style.position = "absolute";
  flashUl.style.width = "100%";
  flashUl.style.height = "60px";
  flashUl.style.padding = "0";
  flashUl.style.margin = "0";

  setTimeout(() => {
    flashUl.style.display = "none";
  }, 5000);
}

document.addEventListener("DOMContentLoaded", stylizeFlashMessages);
