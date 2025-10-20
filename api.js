const BASE = import.meta.env.VITE_API || 'http://localhost:8000'
export const uploadCsv = (file) => fetch(`${BASE}/upload`, { method: 'POST', body: (()=>{ const f=new FormData(); f.append('file', file); return f; })() }).then(r=>r.json())
export const train = (payload) => fetch(`${BASE}/train`, { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)}).then(r=>r.json())
export const metrics = () => fetch(`${BASE}/metrics`).then(r=>r.json())
export const score = () => fetch(`${BASE}/score`, { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({})}).then(r=>r.json())