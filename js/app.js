(function () {
  const materials = window.MATERIALS;
  const groups = window.MATERIAL_GROUPS;

  // Carbon & energy: lower is better. Recyclability: higher is better.
  const DIMENSIONS = [
    { key: "carbon", label: "Carbon score", icon: "cloud", hint: "Relative greenhouse-gas impact", lowerIsBetter: true },
    { key: "recyclability", label: "Recyclability score", icon: "recycle", hint: "Potential for material recovery", lowerIsBetter: false },
    { key: "energy", label: "Energy score", icon: "zap", hint: "Relative production energy demand", lowerIsBetter: true },
  ];

  const SORTS = {
    default: null,
    name: (a, b) => a.name.localeCompare(b.name),
    carbon: (a, b) => a.scores.carbon - b.scores.carbon,
    recyclability: (a, b) => b.scores.recyclability - a.scores.recyclability,
    energy: (a, b) => a.scores.energy - b.scores.energy,
  };

  const state = {
    group: "all",
    query: "",
    sort: "default",
    selectedId: "wood",
  };

  const $ = (sel) => document.querySelector(sel);
  const els = {
    rows: $("#material-rows"),
    filters: $("#filters"),
    search: $("#search"),
    sort: $("#sort"),
    count: $("#catalog-count"),
    summary: $("#catalog-summary"),
    showing: $("#showing"),
    selectedLabel: $("#selected-label"),
    profile: $("#profile"),
    toast: $("#toast"),
  };

  const escapeHtml = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  const isFavourable = (dim, value) => (dim.lowerIsBetter ? value < 50 : value >= 50);

  const swatchStyle = (m) =>
    m.image ? `background-image:url('${m.image}');background-size:cover;background-position:center` : `background:${m.texture}`;

  function hydrateIcons(root = document) {
    root.querySelectorAll("[data-icon]").forEach((el) => {
      el.innerHTML = window.icon(el.dataset.icon, Number(el.dataset.size) || 16);
      el.classList.add("icon-wrap");
      el.removeAttribute("data-icon");
    });
  }

  function visibleMaterials() {
    const q = state.query.trim().toLowerCase();
    const list = materials.filter(
      (m) =>
        (state.group === "all" || m.group === state.group) &&
        (!q || m.name.toLowerCase().includes(q) || m.family.toLowerCase().includes(q))
    );
    const compare = SORTS[state.sort];
    return compare ? list.slice().sort(compare) : list;
  }

  function renderFilters() {
    els.filters.innerHTML = groups
      .map(
        (g) =>
          `<button type="button" class="chip" data-group="${g.id}" aria-pressed="${g.id === state.group}">${escapeHtml(g.label)}</button>`
      )
      .join("");
  }

  function scoreCell(dim, value) {
    const tone = isFavourable(dim, value) ? "good" : "poor";
    return `<span class="score" role="cell" aria-label="${dim.key} ${value} out of 100">
      <span class="score-value">${value}</span>
      <span class="track"><span class="bar ${tone}" style="width:${value}%"></span></span>
    </span>`;
  }

  function renderRows() {
    const list = visibleMaterials();

    if (!list.length) {
      els.rows.innerHTML = `<div class="empty">
        <p>No materials match “${escapeHtml(state.query)}”.</p>
        <button type="button" class="link-button" id="clear-filters">Clear search and filters</button>
      </div>`;
    } else {
      els.rows.innerHTML = list
        .map((m) => {
          const selected = m.id === state.selectedId;
          return `<a class="row material-row${selected ? " is-selected" : ""}" role="row" href="#/materials/${m.id}"
              data-id="${m.id}" ${selected ? 'aria-current="true"' : ""}>
            <span class="identity" role="cell">
              <span class="swatch" style="${swatchStyle(m)}"></span>
              <span class="material-name">${escapeHtml(m.name)}</span>
            </span>
            <span class="family" role="cell">${escapeHtml(m.family)}</span>
            ${DIMENSIONS.map((d) => scoreCell(d, m.scores[d.key])).join("")}
            <span class="row-action" aria-hidden="true">${window.icon(selected ? "arrowRight" : "chevronRight", 16)}</span>
          </a>`;
        })
        .join("");
    }

    els.count.textContent = list.length;
    els.showing.textContent =
      list.length === materials.length
        ? `Showing all ${materials.length} materials`
        : `Showing ${list.length} of ${materials.length} materials`;
  }

  function renderProfile() {
    const m = materials.find((x) => x.id === state.selectedId) || materials[0];
    const chip = /-based$/.test(m.family) ? `${m.family} material` : m.family;

    els.profile.innerHTML = `
      <div class="profile-head">
        <span class="eyebrow">Material profile</span>
        <button type="button" class="icon-button" id="copy-link" title="Copy link to this material" aria-label="Copy link to ${escapeHtml(m.name)}">
          ${window.icon("ellipsis", 18)}
        </button>
      </div>
      <div class="hero" style="${swatchStyle(m)}">
        <span class="hero-chip">${m.group === "other" && m.family === "Plant-based" ? window.icon("sprout", 13) : ""}${escapeHtml(chip)}</span>
      </div>
      <div class="profile-body">
        <div class="profile-title">
          <h2>${escapeHtml(m.name)}</h2>
          <span class="pill">Selected</span>
        </div>
        <p class="profile-description">${escapeHtml(m.description)}</p>

        <div class="env-head">
          <span>Environmental profile</span>
          <span class="illustrative">Illustrative scores</span>
        </div>

        ${DIMENSIONS.map((d) => {
          const v = m.scores[d.key];
          return `<div class="metric">
            <div class="metric-top">
              <span class="metric-label">${window.icon(d.icon, 18)} ${d.label}</span>
              <span class="metric-value">${v}<small> / 100</small></span>
            </div>
            <span class="track track-lg"><span class="bar ${isFavourable(d, v) ? "good" : "poor"}" style="width:${v}%"></span></span>
            <div class="metric-bottom">
              <span>${d.hint}</span>
              <span class="direction">${window.icon(d.lowerIsBetter ? "arrowDown" : "arrowUp", 12)} ${d.lowerIsBetter ? "Lower" : "Higher"} is better</span>
            </div>
          </div>`;
        }).join("")}

        <div class="tradeoff">
          <h3>${window.icon("scanEye", 16)} Read the trade-offs</h3>
          <p>${escapeHtml(m.tradeoff)}</p>
        </div>

        <h3 class="section-title">Before you choose</h3>
        <ul class="tips">
          ${m.tips.map((t) => `<li>${window.icon("arrowUpRight", 14)}<span>${escapeHtml(t)}</span></li>`).join("")}
        </ul>

        <div class="compare">
          <h3 class="section-title">Compare the same function</h3>
          <p>Compare equal function and service life—not just material names. These example indices have no physical units or verified dataset; they are not lifecycle assessment results.</p>
        </div>
      </div>`;

    els.selectedLabel.innerHTML = `${window.icon("circleCheck", 14)} ${escapeHtml(m.name)} selected`;
  }

  function render() {
    renderRows();
    renderProfile();
  }

  let toastTimer;
  function showToast(message) {
    els.toast.textContent = message;
    els.toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => els.toast.classList.remove("is-visible"), 2200);
  }

  // ---- Routing: #/  ·  #/impact  ·  #/materials/<id>
  function route() {
    const hash = location.hash.replace(/^#/, "") || "/";
    const page = hash.startsWith("/impact") ? "impact" : "explorer";

    document.querySelectorAll("[data-page]").forEach((p) => (p.hidden = p.dataset.page !== page));
    document.querySelectorAll("[data-route]").forEach((a) => {
      if (a.dataset.route === page) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });

    const match = hash.match(/^\/materials\/([\w-]+)/);
    if (match && materials.some((m) => m.id === match[1])) {
      const changed = state.selectedId !== match[1];
      state.selectedId = match[1];
      render();
      // On narrow screens the profile sits below the table; bring it into view.
      if (changed && window.matchMedia("(max-width: 1100px)").matches) {
        els.profile.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    } else if (page === "impact") {
      window.scrollTo(0, 0);
    }
  }

  // ---- Events
  els.filters.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-group]");
    if (!btn) return;
    state.group = btn.dataset.group;
    renderFilters();
    renderRows();
  });

  els.search.addEventListener("input", () => {
    state.query = els.search.value;
    renderRows();
  });

  els.sort.addEventListener("change", () => {
    state.sort = els.sort.value;
    renderRows();
  });

  els.rows.addEventListener("click", (e) => {
    if (e.target.closest("#clear-filters")) {
      state.query = "";
      state.group = "all";
      els.search.value = "";
      renderFilters();
      renderRows();
      els.search.focus();
    }
  });

  els.profile.addEventListener("click", async (e) => {
    if (!e.target.closest("#copy-link")) return;
    const url = `${location.href.split("#")[0]}#/materials/${state.selectedId}`;
    try {
      await navigator.clipboard.writeText(url);
      showToast("Link copied");
    } catch {
      showToast(url);
    }
  });

  const isMac = /Mac|iPhone|iPad/.test(navigator.platform);
  $("#search-shortcut").textContent = isMac ? "⌘ K" : "Ctrl K";
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (location.hash.startsWith("#/impact")) location.hash = "#/";
      els.search.focus();
      els.search.select();
    }
  });

  window.addEventListener("hashchange", route);

  // ---- Init
  els.summary.textContent = `${materials.length} materials · ${DIMENSIONS.length} impact dimensions`;
  hydrateIcons();
  renderFilters();
  render();
  route();
})();
