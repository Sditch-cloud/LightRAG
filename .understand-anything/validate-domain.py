import json, os, shutil

with open(r'E:\temp-workspace\LightRAG\.understand-anything\intermediate\domain-analysis.json', encoding='utf-8-sig') as f:
    d = json.load(f)

nodes = d.get('nodes', [])
edges = d.get('edges', [])
domains = [n for n in nodes if n['type'] == 'domain']
flows = [n for n in nodes if n['type'] == 'flow']
steps = [n for n in nodes if n['type'] == 'step']

print(f'Domains: {len(domains)}, Flows: {len(flows)}, Steps: {len(steps)}')
print(f'Edges: {len(edges)}')

# Validate
issues = []
node_ids = {n['id'] for n in nodes}
seen_ids = {}
for i, n in enumerate(nodes):
    if not n.get('id'): issues.append(f'Node[{i}] missing id')
    if not n.get('type'): issues.append(f'Node[{i}] missing type')
    if not n.get('summary'): issues.append(f'Node[{i}] missing summary')
    if not n.get('tags'): issues.append(f'Node[{i}] missing tags')
    if not n.get('complexity'): issues.append(f'Node[{i}] missing complexity')
    if n['id'] in seen_ids: issues.append(f'Duplicate ID: {n["id"]}')
    seen_ids[n['id']] = True

for i, e in enumerate(edges):
    if e.get('source') not in node_ids: issues.append(f'Edge[{i}] source missing: {e.get("source")}')
    if e.get('target') not in node_ids: issues.append(f'Edge[{i}] target missing: {e.get("target")}')
    w = e.get('weight', 0.5)
    try:
        if not (0.0 <= float(w) <= 1.0):
            issues.append(f'Edge[{i}] weight out of range: {w}')
    except:
        issues.append(f'Edge[{i}] invalid weight: {w}')

print(f'Validation issues: {len(issues)}')
for iss in issues[:20]:
    print(' ', iss)

# Auto-fix: drop dangling edges, fill missing fields
if issues:
    edges_fixed = [e for e in edges if e.get('source') in node_ids and e.get('target') in node_ids]
    for n in nodes:
        if not n.get('tags'): n['tags'] = ['untagged']
        if not n.get('summary'): n['summary'] = 'No summary available.'
        if not n.get('complexity'): n['complexity'] = 'moderate'
    d['edges'] = edges_fixed
    print(f'After fix: {len(edges_fixed)} edges (dropped {len(edges) - len(edges_fixed)} dangling)')

# Save domain-graph.json
with open(r'E:\temp-workspace\LightRAG\.understand-anything\domain-graph.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)
size = os.path.getsize(r'E:\temp-workspace\LightRAG\.understand-anything\domain-graph.json')
print(f'domain-graph.json written: {size} bytes')

# Cleanup intermediate files
for fname in ['domain-analysis.json', 'domain-context.json', 'graph-context.json']:
    p = fr'E:\temp-workspace\LightRAG\.understand-anything\intermediate\{fname}'
    if os.path.exists(p):
        os.remove(p)
        print(f'Removed {fname}')

# Remove intermediate dir if empty
try:
    os.rmdir(r'E:\temp-workspace\LightRAG\.understand-anything\intermediate')
    print('Removed intermediate/ directory')
except:
    pass
