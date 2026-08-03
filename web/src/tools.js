export const ENDPOINT = 'https://bible-mcp-server.fly.dev/mcp';

// Mirrors the tool signatures documented in server.py / README.md.
// Each param: { name, type: 'text'|'number'|'checkbox', default, placeholder, help, required }
export const TOOLS = [
  {
    name: 'get_passage',
    description: "Bible text for a reference, e.g. 'John 3:16', 'Genesis 1', 'John 3:16-18'.",
    params: [
      { name: 'reference', type: 'text', required: true, default: 'John 3:16' },
      { name: 'version', type: 'text', default: 'BSB', help: 'BSB, WEB, or any prose work id (Apocrypha needs WEB)' },
    ],
  },
  {
    name: 'search',
    description: 'Full-text search, stemmed and ranked (BM25). Supports quoted phrases and AND/OR/NOT.',
    params: [
      { name: 'query', type: 'text', required: true, default: 'living water' },
      { name: 'version', type: 'text', default: 'BSB' },
      { name: 'book', type: 'text', default: '', help: "optional filter, e.g. 'Psalms'" },
      { name: 'limit', type: 'number', default: 10 },
    ],
  },
  {
    name: 'semantic_search',
    description: 'Meaning-based search across scripture and prose, hybrid-fused with keyword search by default.',
    params: [
      { name: 'query', type: 'text', required: true, default: "self-emptying" },
      { name: 'top_k', type: 'number', default: 5 },
      { name: 'kind', type: 'text', default: '', help: 'optional: verse | window | paragraph' },
      { name: 'hybrid', type: 'checkbox', default: true },
    ],
  },
  {
    name: 'find_similar',
    description: 'Nearest passages by embedding to a given verse or prose paragraph, across every corpus layer.',
    params: [
      { name: 'reference', type: 'text', required: true, default: 'Philippians 2:7' },
      { name: 'top_k', type: 'number', default: 5 },
    ],
  },
  {
    name: 'word_study',
    description: "Original-language word study by Strong's number, lemma, or English gloss.",
    params: [
      { name: 'query', type: 'text', required: true, default: 'G26', help: "Strong's (G26), lemma, or gloss (e.g. 'lovingkindness')" },
      { name: 'language', type: 'text', default: '', help: 'optional: grc | hbo | arc' },
      { name: 'limit', type: 'number', default: 10 },
    ],
  },
  {
    name: 'get_interlinear',
    description: 'Word-by-word original language for a verse or short range.',
    params: [
      { name: 'reference', type: 'text', required: true, default: 'John 1:1' },
    ],
  },
  {
    name: 'get_cross_references',
    description: 'OpenBible.info cross-references for a verse, ranked by community votes, with target text.',
    params: [
      { name: 'reference', type: 'text', required: true, default: 'Romans 5:12' },
      { name: 'limit', type: 'number', default: 10 },
    ],
  },
  {
    name: 'get_citations',
    description: "Where a verse is cited by name in the patristic corpus (translators' footnotes, tier 1).",
    params: [
      { name: 'reference', type: 'text', required: true, default: 'Ephesians 5:21' },
      { name: 'limit', type: 'number', default: 10 },
    ],
  },
  {
    name: 'get_entity',
    description: 'Look up a biblical person, place, event, or people group (Theographic knowledge graph).',
    params: [
      { name: 'name', type: 'text', required: true, default: 'David' },
      { name: 'entity_type', type: 'text', default: '', help: 'optional: person | place | event | people_group' },
    ],
  },
  {
    name: 'entities_in_passage',
    description: 'People, places, and events linked to a verse or chapter.',
    params: [
      { name: 'reference', type: 'text', required: true, default: 'Genesis 14' },
    ],
  },
  {
    name: 'read_work',
    description: 'Read a prose work by paragraph range (Confessions, Imitation of Christ, Apostolic Fathers...).',
    params: [
      { name: 'work', type: 'text', required: true, default: 'CONFESSIONS' },
      { name: 'chapter', type: 'number', default: 1 },
      { name: 'start', type: 'number', default: 1 },
      { name: 'end', type: 'number', default: 3 },
    ],
  },
  {
    name: 'compare_versions',
    description: 'A verse or short range in BSB and WEB, side by side.',
    params: [
      { name: 'reference', type: 'text', required: true, default: 'John 3:16' },
    ],
  },
  {
    name: 'corpus_info',
    description: "What's in the corpus: documents, layers, licenses, and counts.",
    params: [],
  },
];

export async function callTool(name, args) {
  const body = {
    jsonrpc: '2.0',
    id: Math.floor(Math.random() * 1e9),
    method: 'tools/call',
    params: { name, arguments: args },
  };

  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
    },
    body: JSON.stringify(body),
  });

  const raw = await res.text();
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${raw.slice(0, 300)}`);
  }

  // Streamable HTTP frames each response as SSE: "event: message\ndata: {...}\n\n"
  const dataLines = raw
    .split('\n')
    .filter((l) => l.startsWith('data:'))
    .map((l) => l.slice(5).trim());
  if (!dataLines.length) {
    throw new Error('Unexpected response format: ' + raw.slice(0, 300));
  }
  const payload = JSON.parse(dataLines.join(''));

  if (payload.error) {
    throw new Error(payload.error.message || 'Unknown error');
  }
  const result = payload.result;
  if (result?.isError) {
    throw new Error(result.content?.[0]?.text || 'Tool returned an error.');
  }
  return { text: result?.content?.[0]?.text ?? JSON.stringify(result, null, 2), request: body };
}
