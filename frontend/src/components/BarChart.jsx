import React, { useState } from "react";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { Chart } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LinearScale,
  CategoryScale,
  BarElement,
  Legend,
  Tooltip,
  ArcElement,
} from "chart.js";

ChartJS.register(
  LinearScale,
  CategoryScale,
  BarElement,
  Legend,
  Tooltip,
  ArcElement,
  ChartDataLabels
);
ChartJS.defaults.color = "#fff";
ChartJS.defaults.font.size = 14;

const BAR_CHART_OPTIONS = {
  maxBarThickness: 50,
  maintainAspectRatio: false,
  responsive: true,
  scales: {
    y: { ticks: { display: false } },
  },
  plugins: {
    tooltip: {
      callbacks: { label: (context) => ` ${context.parsed.y} votes` },
    },
    legend: {},
    datalabels: {
      anchor: "end",
      display: "auto",
      formatter: function (value, context) {
        return `${value} votes`;
      },
      font: {
        size: 12,
      },
    },
  },
};

const setChartData = (labels, label, dataset) => ({
  labels,
  datasets: [
    {
      type: "bar",
      label: label,
      data: dataset,
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    },
  ],
});

const BarChart = ({ resData }) => {
  const [data] = useState(() =>
    setChartData(resData.labels, resData.title, resData.values)
  );

  return <Chart type="bar" data={data} options={BAR_CHART_OPTIONS} />;
};

export default BarChart;
