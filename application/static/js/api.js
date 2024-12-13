async function fetchData(url, state, party) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ state, party })
  })
  const data = await res.json()
  return data
}