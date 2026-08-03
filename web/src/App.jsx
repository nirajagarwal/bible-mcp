import { useMemo, useState } from 'react'
import { TOOLS, ENDPOINT, callTool } from './tools'
import './App.css'

function defaultsFor(tool) {
  const out = {}
  for (const p of tool.params) out[p.name] = p.default ?? (p.type === 'checkbox' ? false : '')
  return out
}

function ToolForm({ tool, values, onChange }) {
  if (tool.params.length === 0) {
    return <p className="muted">This tool takes no parameters.</p>
  }
  return (
    <div className="form-grid">
      {tool.params.map((p) => (
        <label key={p.name} className="field">
          <span className="field-name">
            {p.name}
            {p.required && <span className="required">*</span>}
          </span>
          {p.type === 'checkbox' ? (
            <input
              type="checkbox"
              checked={!!values[p.name]}
              onChange={(e) => onChange(p.name, e.target.checked)}
            />
          ) : (
            <input
              type={p.type === 'number' ? 'number' : 'text'}
              value={values[p.name]}
              placeholder={p.placeholder || ''}
              onChange={(e) => onChange(p.name, e.target.value)}
            />
          )}
          {p.help && <span className="field-help">{p.help}</span>}
        </label>
      ))}
    </div>
  )
}

export default function App() {
  const [selectedName, setSelectedName] = useState(TOOLS[0].name)
  const tool = useMemo(() => TOOLS.find((t) => t.name === selectedName), [selectedName])
  const [values, setValues] = useState(defaultsFor(tool))
  const [loading, setLoading] = useState(false)
  const [slow, setSlow] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [request, setRequest] = useState(null)

  function selectTool(name) {
    setSelectedName(name)
    const t = TOOLS.find((x) => x.name === name)
    setValues(defaultsFor(t))
    setResult(null)
    setError(null)
    setRequest(null)
  }

  function updateValue(name, val) {
    setValues((v) => ({ ...v, [name]: val }))
  }

  async function run() {
    setLoading(true)
    setSlow(false)
    setError(null)
    setResult(null)
    // The Fly machine scales to zero when idle, so an occasional request pays a
    // cold-start cost. Only surface that explanation if it's actually happening,
    // not on every (usually fast) request.
    const slowTimer = setTimeout(() => setSlow(true), 2500)
    try {
      const args = {}
      for (const p of tool.params) {
        const raw = values[p.name]
        if (p.type === 'number') {
          if (raw !== '' && raw !== undefined) args[p.name] = Number(raw)
        } else if (p.type === 'checkbox') {
          args[p.name] = !!raw
        } else if (raw !== '' && raw !== undefined) {
          args[p.name] = raw
        }
      }
      const { text, request } = await callTool(tool.name, args)
      setResult(text)
      setRequest(request)
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      clearTimeout(slowTimer)
      setLoading(false)
      setSlow(false)
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <h1>bible-mcp</h1>
        <p className="tagline">
          An MCP server for Christian scholarship and research — scripture, Greek/Hebrew word
          data, cross-references, patristic texts, and semantic search, queryable by any MCP
          client.
        </p>
        <div className="links">
          <a href="https://github.com/nirajagarwal/bible-mcp" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a href={ENDPOINT} target="_blank" rel="noreferrer">
            Live endpoint
          </a>
          <a
            href="https://registry.modelcontextprotocol.io/v0/servers?search=bible-mcp"
            target="_blank"
            rel="noreferrer"
          >
            MCP Registry
          </a>
        </div>
      </header>

      <section className="panel">
        <h2>Try it live</h2>
        <p className="muted">
          Calls the live server at <code>{ENDPOINT}</code>
        </p>
        <div className="demo">
          <div className="tool-list">
            {TOOLS.map((t) => (
              <button
                key={t.name}
                className={'tool-btn' + (t.name === selectedName ? ' active' : '')}
                onClick={() => selectTool(t.name)}
              >
                {t.name}
              </button>
            ))}
          </div>

          <div className="tool-detail">
            <h3>{tool.name}</h3>
            <p className="muted">{tool.description}</p>
            <ToolForm tool={tool} values={values} onChange={updateValue} />
            <button className="run-btn" onClick={run} disabled={loading}>
              {loading ? 'Running…' : 'Run'}
            </button>
            {loading && slow && (
              <p className="muted wake-note">
                Waking up the server — it scales to zero when idle, so the first request
                after a quiet spell can take up to ~15s. It'll be fast from here.
              </p>
            )}

            {error && (
              <div className="result error">
                <div className="result-line">{error}</div>
              </div>
            )}
            {result && (
              <div className="result">
                {result.split('\n').map((line, i) => (
                  <div key={i} className="result-line">
                    {line || ' '}
                  </div>
                ))}
              </div>
            )}
            {request && (
              <details className="request-details">
                <summary>Request sent</summary>
                <pre>{JSON.stringify(request, null, 2)}</pre>
              </details>
            )}
          </div>
        </div>
      </section>

      <section className="panel">
        <h2>Use it in your own client</h2>
        <div className="use-grid">
          <div>
            <h3>Remote (no install)</h3>
            <p>
              Add <code>{ENDPOINT}</code> as a custom connector in any MCP client. In Claude:
              Settings → Connectors → Add custom connector.
            </p>
          </div>
          <div>
            <h3>Local (stdio)</h3>
            <p>
              Clone the repo, download <code>db/bible.db</code> from the latest GitHub Release,
              and point your MCP config at <code>server.py</code>.
            </p>
          </div>
          <div>
            <h3>Self-host</h3>
            <p>
              The repo ships a <code>Dockerfile</code> for the Streamable-HTTP server — see{' '}
              <code>DEPLOY.md</code> for the full runbook.
            </p>
          </div>
        </div>
      </section>

      <section className="panel">
        <h2>What's in the corpus</h2>
        <ul className="source-list">
          <li>Berean Standard Bible (66 books) &amp; World English Bible with Apocrypha (83 books)</li>
          <li>613,690 original-language words: Greek NT + Hebrew/Aramaic OT with lemmas, Strong's, morphology, glosses</li>
          <li>~345,000 ranked cross-references (openbible.info)</li>
          <li>~4,800 people/places/events/groups + 53,000 verse links (Theographic)</li>
          <li>Patristic texts: the Apostolic Fathers, Irenaeus' Against Heresies, Justin Martyr</li>
          <li>Six public-domain classics: Augustine, à Kempis, Bunyan, Brother Lawrence, Julian of Norwich, Chesterton</li>
          <li>A tier-1 citation graph extracted from translators' own footnotes</li>
          <li>~55,800 embeddings for semantic + hybrid search across every layer</li>
        </ul>
        <p className="muted">
          Full source/license table in the{' '}
          <a href="https://github.com/nirajagarwal/bible-mcp#readme" target="_blank" rel="noreferrer">
            README
          </a>
          .
        </p>
      </section>

      <footer className="footer">
        <p>
          Non-commercial public resource. Sources keep their own licenses (PD / CC BY / CC
          BY-SA); code is PolyForm Noncommercial 1.0.0; derived data is CC BY-NC 4.0. See{' '}
          <a href="https://github.com/nirajagarwal/bible-mcp/blob/master/LICENSE.md" target="_blank" rel="noreferrer">
            LICENSE.md
          </a>{' '}
          and{' '}
          <a href="https://github.com/nirajagarwal/bible-mcp/blob/master/NOTICE.md" target="_blank" rel="noreferrer">
            NOTICE.md
          </a>
          .
        </p>
      </footer>
    </div>
  )
}
