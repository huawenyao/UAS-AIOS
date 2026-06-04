const navLinks = Array.from(document.querySelectorAll(".nav a"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

let demoState = null;

const byId = (id) => document.getElementById(id);

const activateCurrentSection = () => {
  const current = sections
    .map((section) => ({
      id: section.id,
      offset: Math.abs(section.getBoundingClientRect().top - 120),
    }))
    .sort((a, b) => a.offset - b.offset)[0];

  if (!current) return;

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${current.id}`);
  });
};

const recommendationLabel = {
  strong: "Strong",
  review: "Review",
  caution: "Caution",
};

function renderMetrics(state) {
  byId("metric-qualified-shortlist").textContent = state.metrics.qualifiedShortlist;
  byId("metric-evidence-coverage").textContent = state.metrics.evidenceCoverage;
  byId("metric-hm-satisfaction").textContent = state.metrics.hmSatisfaction;
  byId("metric-bias-risk").textContent = state.metrics.biasRisk;
}

function renderCandidateList(state) {
  const list = byId("candidate-list");
  list.innerHTML = `
    <div class="candidate-row header">
      <span>Candidate</span>
      <span>Recommendation</span>
      <span>Evidence</span>
      <span>Risk</span>
      <span>Action</span>
    </div>
  `;

  state.candidates.forEach((candidate) => {
    const row = document.createElement("div");
    row.className = "candidate-row";
    row.innerHTML = `
      <span><b>${candidate.name}</b><small>${candidate.candidate_id}</small></span>
      <span class="badge ${candidate.recommendation}">${recommendationLabel[candidate.recommendation]}</span>
      <span>${candidate.top_evidence}</span>
      <span>${candidate.risk}</span>
      <button>${candidate.recommendation === "strong" ? "Advance" : "Review"}</button>
    `;
    list.appendChild(row);
  });
}

function renderAgentRunLog(state) {
  const log = byId("agent-run-log");
  log.innerHTML = "";

  state.agentRunLog.forEach((item) => {
    const entry = document.createElement("div");
    entry.className = "log-item";
    entry.innerHTML = `
      <span>${item.agent}</span>
      <strong>${item.capability}</strong>
      <span class="${item.confirmation ? "confirmation" : ""}">
        ${item.confirmation ? "Human confirmation" : "Auto evidence step"}
      </span>
    `;
    log.appendChild(entry);
  });
}

function runAgentJourney() {
  if (!demoState) return;
  renderMetrics(demoState);
  renderCandidateList(demoState);
  renderAgentRunLog(demoState);
}

async function loadDemoState() {
  const response = await fetch('./data/demo_state.json');
  demoState = await response.json();
  runAgentJourney();
}

document.addEventListener("scroll", activateCurrentSection, { passive: true });
byId("run-agent-journey").addEventListener("click", runAgentJourney);
activateCurrentSection();
loadDemoState();
