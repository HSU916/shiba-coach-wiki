document.addEventListener("DOMContentLoaded", () => {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const searchInput = document.getElementById("wikiSearch");
  const cards = document.querySelectorAll("#wikiCards .card");
  const emptyState = document.getElementById("emptyState");

  let activeCategory = "all";

  function applyFilter() {
    const keyword = (searchInput ? searchInput.value : "").trim().toLowerCase();
    let visibleCount = 0;

    cards.forEach((card) => {
      const cat = card.dataset.category || "";
      const text = card.textContent.toLowerCase();
      const matchCategory = activeCategory === "all" || cat === activeCategory;
      const matchKeyword = !keyword || text.includes(keyword);

      if (matchCategory && matchKeyword) {
        card.style.display = "flex";
        visibleCount += 1;
      } else {
        card.style.display = "none";
      }
    });

    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeCategory = btn.dataset.filter || "all";
      applyFilter();
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", applyFilter);
  }
});
