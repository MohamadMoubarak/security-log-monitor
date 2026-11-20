let token = null;
let chart = null;

const loginSection = document.getElementById("login-section");
const dashboard = document.getElementById("dashboard");
const loginError = document.getElementById("login-error");

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new URLSearchParams();
    form.append("username", document.getElementById("username").value);
    form.append("password", document.getElementById("password").value);

    const response = await fetch("/login", { method: "POST", body: form});
    if(!response.ok) {
        loginError.textContent = "Wrong username or password";
        return;
    }
    const data = await response.json();
    token = data.access_token;
    loginError.textContent = "";
    loginSection.hidden = true;
    dashboard.hidden = false;
    loadDashboard();
});

document.getElementById("logout").addEventListener("click", () => {
    token = null;
    dashboard.hidden = true;
    loginSection.hidden = false;
});

async function apiGet(path) {
    const response = await fetch(path, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 401) {
        document.getElementById("logout").click();
        throw new Error("Session expired");
    }
    return response.json();
}

function fillTable(tableId, rows, columns) {
  const tbody = document.querySelector(`#${tableId} tbody`);
  tbody.replaceChildren();
  for (const row of rows) {
    const tr = document.createElement("tr");
    for (const column of columns) {
      const td = document.createElement("td");
      td.textContent = row[column];
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
}

function drawChart(events) {
  const failuresByIp = {};
  for (const e of events) {
    if (e.status === "failed") {
      failuresByIp[e.ip] = (failuresByIp[e.ip] || 0) + 1;
    }
  }
  if (chart) chart.destroy();
  chart = new Chart(document.getElementById("chart"), {
    type: "bar",
    data: {
      labels: Object.keys(failuresByIp),
      datasets: [{ label: "Failed logins", data: Object.values(failuresByIp) }],
    },
  });
}

async function loadDashboard() {
  const alerts = await apiGet("/alerts");
  const events = await apiGet("/events");
  document.getElementById("alert-count").textContent = alerts.length;
  document.getElementById("event-count").textContent = events.length;
  fillTable("alerts-table", alerts, ["ip", "failures", "first_seen", "last_seen"]);
  fillTable("events-table", events, ["time", "status", "username", "ip", "port"]);
  drawChart(events);
}