# CreateChart 0.1.1

Ready-to-use release for GitHub Profile charts.

## What's included

- 28 pure SVG chart cards with Chinese and English labels
- Offline demo mode with standalone `preview.html`
- Real GitHub mode using the GitHub REST API
- CLI entry point: `createchart`
- `Release/createchart-0.1.1.zip` source archive

## Install

```bash
python3 -m pip install -e .
```

## Offline preview

```bash
createchart --demo --preview-html --lang zh -o charts-zh
```

Open `charts-zh/preview.html`.

## Real GitHub data

```bash
export GITHUB_TOKEN=ghp_xxx
createchart octocat --lang zh -o charts
```

Then embed any generated SVG in a GitHub Profile README:

```markdown
![Profile stats](charts/profile.svg)
```

## Verify

```bash
python3 -m pytest -q
```

Author: 科技酱 (https://www.asoe.cn)
