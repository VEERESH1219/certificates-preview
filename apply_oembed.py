import os
import glob
import json
import re

# correct base url for preview
BASE_URL = "https://veeresh1219.github.io/certificates-preview/bootcamp/kiet"

docs_dir = os.path.join(os.path.dirname(__file__), "docs", "bootcamp", "kiet")
pattern = os.path.join(docs_dir, "*", "index.html")
files = glob.glob(pattern)

count = 0

for filepath in files:
    # Skip share page
    if "share" in filepath.lower():
        continue
        
    folder_path = os.path.dirname(filepath)
    student_id = os.path.basename(folder_path)
    
    # 1. Read index.html
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # extract title just to be safe/nice in the oembed
    title_match = re.search(r'<meta property="og:title" content="(.*?)">', content)
    title = title_match.group(1) if title_match else f"Certificate - {student_id}"

    # 2. Check if oembed link exists, if not, inject it
    if "application/json+oembed" not in content:
        oembed_url = f"{BASE_URL}/{student_id}/oembed.json"
        link_tag = f'\n    <link rel="alternate" type="application/json+oembed" href="{oembed_url}" title="{title}" />'
        
        # Inject before </head>
        new_content = content.replace("</head>", f"{link_tag}\n</head>")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    
    # 3. Create oembed.json
    oembed_data = {
        "type": "photo",
        "version": "1.0",
        "title": title,
        "author_name": "AI Karyashala",
        "author_url": "https://aikaryashala.com",
        "provider_name": "AI Karyashala", 
        "provider_url": "https://aikaryashala.com",
        "cache_age": 3600,
        "url": f"{BASE_URL}/{student_id}/preview.jpg",
        "width": 1200,
        "height": 630
    }
    
    json_path = os.path.join(folder_path, "oembed.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(oembed_data, f, indent=2)
        
    count += 1
    if count % 50 == 0:
        print(f"Processed {count} students...")

print(f"Done! Processed {count} students.")
