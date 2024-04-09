const dashboardSlug = document
  .getElementById("dashboard-slug")
  .textContent.trim();
const submitBtn = document.getElementById("submit-btn");
const dataInput = document.getElementById("data-input");
const user = document.getElementById("user").innerText;
const dataList = document.getElementById("data-list");

const ctx = document.getElementById("chart");
const chartData = JSON.parse(document.getElementById("chart-data").textContent);
const chartLabels = JSON.parse(
  document.getElementById("chart-labels").textContent
);

let pieChart;

const socket = new WebSocket(
  `ws://${window.location.host}/ws/${dashboardSlug}/`
);

socket.onmessage = function (e) {
  let parseData = JSON.parse(e.data);
  const { message, sender, chart_data, chart_labels } = parseData;

  overwriteData(pieChart, chart_data, chart_labels);

  let li = document.createElement("li");
  li.classList.add("list-group-item");
  li.textContent = `${sender}: ${message}`;
  dataList.appendChild(li);
};

submitBtn.addEventListener("click", () => {
  const dataValue = dataInput.value;
  console.log(user);

  socket.send(
    JSON.stringify({
      message: dataValue,
      sender: user,
    })
  );

  dataInput.value = "";
});

const drawChart = () => {
  pieChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: chartLabels,
      datasets: [
        {
          label: `Contributed`,
          data: chartData,
          // backgroundColor: Object.values(Utils.CHART_COLORS),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: `${dashboardSlug} Pie Chart`,
        },
      },
    },
  });
};

drawChart();

function overwriteData(chart, newData, newLabels) {
  chart.data.datasets.forEach((dataset, index) => {
    dataset.data = newData;
    chart.data.labels = newLabels;
    delete dataset.backgroundColor;
  });
  chart.update();
}

// socket.onopen = function(e){
//     socket.send(JSON.stringify({
//         'message': 'Hi from client',
//         'sender': 'test-user',
//     }));
// };
