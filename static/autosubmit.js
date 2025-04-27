
document.addEventListener("DOMContentLoaded", () => {
  const options = document.querySelectorAll("input[type='radio']");
  options.forEach(opt => {
    opt.addEventListener("change", () => {
      const form = opt.closest("form");
      if (form) form.submit();
    });
  });
});
