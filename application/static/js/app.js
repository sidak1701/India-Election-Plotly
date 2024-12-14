async function handleSubmit() {
  const stateEl = document.getElementsByName('state')[0]
  const partyEl = document.getElementsByName('party')[0]

  const state = stateEl.value
  const party = partyEl.value

  await updateMapBox(state, party)
  await updateBarChart(state, party)
  await updateBarChart2(state, party)
  await updatePieChart(state, party)
}

async function updateMapBox(state, party) {
  const res = await fetchData('/map', state, party)
  console.log("🚀 ~ updateMapBox ~ res:", res)
  const { data, layout } = JSON.parse(res)
  Plotly.newPlot("map-box", data, layout);
}

async function updateBarChart(state, party) {
  const res = await fetchData('/barchart', state, party)
  const { data, layout } = JSON.parse(res)
  Plotly.newPlot("bar-chart", data, layout);
}

async function updateBarChart2(state, party) {
  const res = await fetchData('/barchart2', state, party)
  const { data, layout } = JSON.parse(res)
  Plotly.newPlot("bar-chart2", data, layout);
}

async function updatePieChart(state, party) {
  const res = await fetchData('/piechart', state, party)
  const { data, layout } = JSON.parse(res)
  Plotly.newPlot("pie-chart", data, layout);
}

updateMapBox('', '')
updateBarChart('', '')
updateBarChart2('', '')
updatePieChart('', '')