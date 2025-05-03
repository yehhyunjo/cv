import json
import os

def format_authors(authors_list):
    if not authors_list:
        return "Anonymous"

    formatted = []
    for author in authors_list:
        name = author.get('credit-name', {}).get('value')
        if not name:
            given = author.get('given-names', {}).get('value', '')
            family = author.get('family-name', {}).get('value', '')
            name = f"{given} {family}"
        parts = name.split()
        if len(parts) >= 2:
            formatted.append(f"{parts[0][0]}. {' '.join(parts[1:])}")
        else:
            formatted.append(name)
    if len(formatted) > 1:
        return ', '.join(formatted[:-1]) + ' & ' + formatted[-1]
    return formatted[0]

def format_reference(entry, i):
    title = entry.get('title', {}).get('title', {}).get('value', 'No title')
    journal = entry.get('journal-title', {}).get('value', '')
    pub_date = entry.get('publication-date', {})
    year = pub_date.get('year', {}).get('value', 'n.d.')
    authors = entry.get('contributors', {}).get('contributor', [])
    doi = ''
    for ext_id in entry.get('external-ids', {}).get('external-id', []):
        if ext_id.get('external-id-type') == 'doi':
            doi = ext_id.get('external-id-value')
            break

    formatted_authors = format_authors(authors)
    ref = f"{i+1}. {formatted_authors}. \"{title}\" *{journal}* **{year}**"
    if doi:
        ref += f". [https://doi.org/{doi}](https://doi.org/{doi})"
    return ref

# Load ORCID data
with open("orcid_works.json", "r") as f:
    data = json.load(f)

works = data['group']
refs = []

# Extract & sort by year descending
entries = [work['work-summary'][0] for work in works]
entries = sorted(entries, key=lambda w: w.get('publication-date', {}).get('year', {}).get('value', '0'), reverse=True)

# Generate formatted reference list
for i, entry in enumerate(entries):
    refs.append(format_reference(entry, i))

# Save to Markdown file
output_path = "content/publication/publications.md"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    f.write("---\ntitle: Publications\nlayout: default\n---\n\n")
    f.write("# 📚 Publications (Auto-synced from ORCID)\n\n")
    for ref in refs:
        f.write(f"{ref}\n\n")

print(f"✅ Successfully wrote {len(refs)} Nature-style references to {output_path}")
