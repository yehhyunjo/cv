curl https://pub.orcid.org/v3.0/0000-0003-4731-240X/works \
  -H "Accept: application/json" \
  -o orcid_works.json

import json
import os
import requests

with open("orcid_works.json", "r") as f:
    data = json.load(f)

works = data['group']

output_dir = "content/publication/"
os.makedirs(output_dir, exist_ok=True)

for i, work in enumerate(works):
    work_summary = work['work-summary'][0]
    title = work_summary.get('title', {}).get('title', {}).get('value', 'No Title')
    pub_date = work_summary.get('publication-date', {})
    year = pub_date.get('year', {}).get('value', 'n.d.')
    doi = ''
    for ext_id in work_summary.get('external-ids', {}).get('external-id', []):
        if ext_id.get('external-id-type') == 'doi':
            doi = ext_id.get('external-id-value')
            break

    filename = os.path.join(output_dir, f"{i:03d}-{title.lower().replace(' ', '_').replace('/', '-')[:40]}.md")
    
    with open(filename, 'w') as out:
        out.write(f"""---
title: "{title}"
date: {year}-01-01
doi: "https://doi.org/{doi}"
publication_types: ["2"]
authors: []
publication: ""
---

""")

print("✅ ORCID publications exported to Markdown.")
