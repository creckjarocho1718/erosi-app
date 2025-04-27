document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.progress-bar').forEach(pb => {
    const p = pb.getAttribute('data-percent');
    if (p) {
      // delay to allow layout
      setTimeout(() => {
        pb.style.width = p + '%';
      }, 100);
    }
  });
});