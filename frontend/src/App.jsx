import React, { useState } from 'react'
import { uploadCsv, train, metrics, score } from './api'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

export default function App() {
  const [cols, setCols] = useState([])
  const [rows, setRows] = useState(0)
  const [auc, setAuc] = useState(null)
  const [churnRate, setChurnRate] = useState(null)
  const [top, setTop] = useState([])
  const [scores, setScores] = useState([])
  const [target, setTarget] = useState('churn')

  const onUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const res = await uploadCsv(file)
    setCols(res.columns || [])
    setRows(res.rows || 0)
  }

  const onTrain = async () => {
    const res = await train({ target, id_column: 'customer_id' })
    setAuc(res.auc)
  }

  const onMetrics = async () => {
    const m = await metrics()
    setChurnRate(m.churn_rate)
    setTop(m.top_features || [])
  }

  const onScore = async () => {
    const s = await score()
    setScores(s.scores || [])
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">AI CRM Insight Dashboard</h1>
        <a href="https://github.com/" className="text-sm underline">
          GitHub (add later)
        </a>
      </header>

      {/* Upload section */}
      <section className="bg-white p-4 rounded-2xl shadow">
        <h2 className="font-semibold mb-2">1) Upload CSV</h2>
        <input type="file" accept=".csv" onChange={onUpload} className="block" />
        {rows > 0 && (
          <p className="text-sm text-gray-600 mt-2">
            Loaded {rows} rows · Columns: {cols.join(', ')}
          </p>
        )}
      </section>

      {/* Train + Metrics */}
      <section className="bg-white p-4 rounded-2xl shadow grid md:grid-cols-2 gap-4">
        <div>
          <h2 className="font-semibold mb-2">2) Train</h2>
          <label className="text-sm">Target column</label>
          <input
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            className="border rounded px-2 py-1 ml-2"
          />
          <button
            onClick={onTrain}
            className="ml-2 px-3 py-1 rounded bg-gray-900 text-white"
          >
            Train
          </button>
          {auc !== null && (
            <p className="text-sm text-gray-600 mt-2">
              AUC: {auc?.toFixed ? auc.toFixed(3) : auc}
            </p>
          )}
        </div>

        <div>
          <h2 className="font-semibold mb-2">3) Metrics</h2>
          <button
            onClick={onMetrics}
            className="px-3 py-1 rounded bg-gray-900 text-white"
          >
            Refresh
          </button>
          {churnRate !== null && (
            <p className="text-sm text-gray-600 mt-2">
              Churn rate: {(churnRate * 100).toFixed(1)}%
            </p>
          )}
          <div className="h-56 mt-2">
            <ResponsiveContainer>
              <LineChart
                data={top.map((t, i) => ({ i, w: t.weight, name: t.name }))}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="i" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="w" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Score + Recommendations */}
      <section className="bg-white p-4 rounded-2xl shadow">
        <h2 className="font-semibold mb-2">4) Score & Recommendations</h2>
        <button
          onClick={onScore}
          className="px-3 py-1 rounded bg-gray-900 text-white"
        >
          Score all
        </button>

        <div className="overflow-auto mt-3">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left">
                <th className="p-2">Customer</th>
                <th className="p-2">Prob</th>
                <th className="p-2">Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {scores.map((s, idx) => (
                <tr key={idx} className="border-t">
                  <td className="p-2">{s.customer_id || s.index}</td>
                  <td className="p-2">{(s.prob * 100).toFixed(1)}%</td>
                  <td className="p-2">{s.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <footer className="text-xs text-gray-500">
        MVP for internship portfolio • FastAPI + React + ML
      </footer>
    </div>
  )
}
