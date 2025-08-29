#!/usr/bin/env python3
"""
Script to generate an HTML page from README.md links in the "C2 vs GraalJIT Benchmarking Results" section.
"""

import re
from datetime import datetime
from pathlib import Path

def parse_readme_links():
    """Parse links from the README.md file under the C2 vs GraalJIT Benchmarking Results section."""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found in current directory")
    
    content = readme_path.read_text()
    
    # Find the section and extract links
    section_pattern = r"# C2 vs GraalJIT Benchmarking Results\s*\n(.*?)(?=\n#|\Z)"
    section_match = re.search(section_pattern, content, re.DOTALL)
    
    if not section_match:
        raise ValueError("Could not find 'C2 vs GraalJIT Benchmarking Results' section")
    
    section_content = section_match.group(1)
    
    # Extract markdown links
    link_pattern = r"- \[([^\]]+)\]\(([^)]+)\)"
    links = re.findall(link_pattern, section_content)
    
    parsed_links = []
    for title, url in links:
        parsed_link = parse_link_info(title, url)
        if parsed_link:
            parsed_links.append(parsed_link)
    
    return parsed_links

def parse_link_info(title, url):
    """Parse information from link title and URL."""
    # Extract Java version
    java_match = re.search(r"Java (\d+)", title)
    java_version = java_match.group(1) if java_match else "Unknown"
    
    # Extract benchmark suite
    suite = "Unknown"
    if "Microbenchmarks" in title or "OpenJDK" in title:
        suite = "OpenJDK Micro Benchmarks"
    elif "Renaissance" in title:
        suite = "Renaissance"
    elif "SPEC JVM" in title:
        suite = "SPEC JVM 2008"
    
    # Extract architecture
    arch = "Unknown"
    arch_display = "Unknown"
    if "x64" in title or "intel" in url:
        arch = "x86_64"
        arch_display = "x86_64"
    elif "Aarch64" in title or "AArch64" in title or "arm" in url:
        arch = "AArch64"
        arch_display = "AArch64"
    
    # Extract date from URL
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", url)
    date = date_match.group(1) if date_match else "Unknown"
    
    # Patch URL to point to index.html
    patched_url = url.rstrip('/') + '/index.html'
    
    # Read title from target README.md
    readme_title = read_target_readme_title(url)
    
    return {
        "title": title,
        "readme_title": readme_title,
        "url": patched_url,
        "java_version": java_version,
        "suite": suite,
        "arch": arch,
        "arch_display": arch_display,
        "date": date
    }

def read_target_readme_title(url):
    """Read the title from the target folder's README.md file."""
    try:
        # Remove leading './' if present and construct README path
        clean_url = url.lstrip('./')
        readme_path = Path(clean_url) / "README.md"
        
        if readme_path.exists():
            content = readme_path.read_text()
            # Look for ### Title section
            title_match = re.search(r"### Title\s*\n(.+)", content)
            if title_match:
                return title_match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not read title from {url}: {e}")
    
    return "Benchmark Comparison Report"

def group_links_by_suite_and_java(links):
    """Group links by benchmark suite and Java version."""
    grouped = {}
    
    for link in links:
        suite = link["suite"]
        java_version = link["java_version"]
        
        if suite not in grouped:
            grouped[suite] = {}
        
        if java_version not in grouped[suite]:
            grouped[suite][java_version] = []
        
        grouped[suite][java_version].append(link)
    
    return grouped

def generate_html(grouped_links):
    """Generate HTML content based on the grouped links."""
    
    # Build the sections HTML first
    sections_html = build_sections_html(grouped_links)
    
    # Create the complete HTML
    html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenJDK HotSpot vs GraalVM JIT — Benchmark Results</title>
  <style>
    :root{{
      --bg: #0b0e12;
      --card: #11161d;
      --muted: #8aa0b6;
      --text: #e7edf5;
      --accent: #6bc2ff;
      --accent-2: #9dffb0;
      --chip: #1a2330;
      --chip-border: #263244;
      --shadow: 0 10px 30px rgba(0,0,0,.35);
      --radius: 16px;
    }}
    @media (prefers-color-scheme: light){{
      :root{{
        --bg:#f6f8fb; --card:#ffffff; --muted:#546e7a; --text:#0b1a2b; --chip:#eef4fb; --chip-border:#d3e2f0; --accent:#006dff; --accent-2:#009c6b; --shadow:0 10px 30px rgba(0,0,0,.08);
      }}
    }}
    *{{box-sizing:border-box}}
    html,body{{height:100%}}
    body{{
      margin:0; font:500 16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial,sans-serif; background:var(--bg); color:var(--text);
    }}
    header{{
      position:sticky; top:0; z-index:10; backdrop-filter:saturate(1.2) blur(8px);
      background:linear-gradient(180deg, rgba(11,14,18,.85), rgba(11,14,18,.6));
      border-bottom:1px solid rgba(255,255,255,.06);
    }}
    .container{{max-width:1100px; margin:0 auto; padding:20px 20px 32px}}
    .hero{{display:flex; align-items:center; gap:16px; padding:6px 0 8px}}
    .hero svg{{flex:0 0 auto}}
    h1{{font-weight:800; letter-spacing:.2px; font-size:clamp(22px,3vw,28px); margin:0}}
    .subtitle{{color:var(--muted); font-size:14px; margin-top:4px}}

    .grid{{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px; margin-top:22px}}
    .card{{
      background:var(--card); border:1px solid rgba(255,255,255,.06); border-radius:var(--radius); padding:18px; box-shadow:var(--shadow);
      transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease
    }}
    .card:hover{{transform:translateY(-2px); box-shadow:0 16px 40px rgba(0,0,0,.28); border-color:rgba(255,255,255,.14)}}
    .card h2{{font-size:18px; margin:0 0 12px}}

    .chips{{display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px}}
    .chip{{
      display:inline-flex; align-items:center; gap:6px; padding:6px 10px; background:var(--chip); border:1px solid var(--chip-border); border-radius:999px; font-size:12px; color:var(--muted)
    }}
    .chip strong{{color:var(--text); font-weight:700}}

    .links{{display:flex; flex-direction:column; gap:10px}}
    .link{{
      display:flex; justify-content:space-between; align-items:center; gap:10px;
      padding:12px 14px; border-radius:12px; border:1px solid rgba(255,255,255,.06);
      text-decoration:none; color:var(--text); background:linear-gradient(0deg, rgba(255,255,255,.02), rgba(255,255,255,.0));
      transition:background .18s ease, border-color .18s ease, transform .18s ease
    }}
    .link:hover{{background:linear-gradient(0deg, rgba(255,255,255,.06), rgba(255,255,255,.0)); border-color:rgba(255,255,255,.14); transform:translateY(-1px)}}
    .link .left{{display:flex; align-items:center; gap:12px}}
    .arch{{display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--muted); padding:4px 8px; border-radius:999px; border:1px dashed var(--chip-border)}}
    .date{{font-size:12px; color:var(--muted)}}

    .suite{{display:flex; align-items:center; gap:10px}}
    .badge{{font-size:11px; padding:3px 8px; border-radius:999px; border:1px solid currentColor; opacity:.9}}
    .badge.acc{{color:var(--accent)}}
    .badge.ok{{color:var(--accent-2)}}

    footer{{opacity:.8; color:var(--muted); font-size:12px; margin-top:28px}}

    /* Tiny utility to space sections */
    section{{margin-top:18px}}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <div class="hero">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <div>
          <h1>OpenJDK HotSpot vs GraalVM JIT — Benchmark Results</h1>
          <div class="subtitle">Curated links to side‑by‑side comparisons by suite, Java version, and architecture.</div>
        </div>
      </div>
    </div>
  </header>

  <main class="container">
{sections_html}
    <footer>
      Tip: Right‑click a link and open in a new tab to compare multiple reports side‑by‑side.
    </footer>
  </main>

  <script>
    // Pretty-print ISO dates as "Updated Aug 26, 2025" and add relative title
    (function(){{
      const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
      document.querySelectorAll('.date[data-date]').forEach(function(el){{
        const iso = el.getAttribute('data-date');
        const d = new Date(iso + 'T12:00:00');
        if(!isNaN(d)){{
          const label = 'Updated ' + months[d.getUTCMonth()] + ' ' + d.getUTCDate() + ', ' + d.getUTCFullYear();
          el.textContent = label;
          const days = Math.round((Date.now() - d.getTime())/86400000);
          el.title = days === 0 ? 'today' : days + ' day' + (days!==1?'s':'') + ' ago';
        }}
      }});
    }})();
  </script>
</body>
</html>"""
    
    return html_content

def build_sections_html(grouped_links):
    """Build the sections HTML separately to avoid formatting issues."""

    sections_html = ""
    
    # Define suite badges and order
    suite_info = {
        "Renaissance": {"badge_class": "acc", "title": "High-level, modern JVM benchmark suite"},
        "OpenJDK Micro Benchmarks": {"badge_class": "ok", "title": "JMH-based microbenchmarks"},
        "SPEC JVM 2008": {"badge_class": "acc", "title": "Standard Performance Evaluation Corporation JVM benchmark"}
    }
    
    # Process each suite
    for suite_name in ["Renaissance", "OpenJDK Micro Benchmarks", "SPEC JVM 2008"]:
        if suite_name not in grouped_links:
            continue
            
        suite_data = grouped_links[suite_name]
        badge_info = suite_info.get(suite_name, {"badge_class": "acc", "title": "Benchmark suite"})
        
        sections_html += f'''    <!-- {suite_name} -->
    <section class="card">
      <div class="suite">
        <h2 style="margin:0">{suite_name}</h2>
        <span class="badge {badge_info["badge_class"]}" title="{badge_info["title"]}">SUITE</span>
      </div>
      <div class="grid">
'''
        
        # Sort Java versions (newest first)
        java_versions = sorted(suite_data.keys(), key=lambda x: int(x) if x.isdigit() else 0, reverse=True)
        
        for java_version in java_versions:
            links = suite_data[java_version]
            lts_label = " (LTS)" if java_version == "21" else ""
            
            sections_html += f'''        <!-- Java {java_version} card -->
        <div class="card">
          <div class="chips">
            <span class="chip"><strong>Java</strong> {java_version}{lts_label}</span>
            <span class="chip">HotSpot vs GraalVM</span>
          </div>
          <div class="links">
'''
            
            # Sort links by architecture (x86_64 first, then AArch64)
            arch_order = {"x86_64": 0, "AArch64": 1}
            sorted_links = sorted(links, key=lambda x: arch_order.get(x["arch"], 2))
            
            for link in sorted_links:
                arch_title = "x86_64 (Intel/AMD)" if link["arch"] == "x86_64" else "AArch64 (Arm)"
                sections_html += f'''            <a class="link" href="{link["url"]}">
              <div class="left">
                <span class="arch" title="{arch_title}">
                  <!-- CPU icon -->
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><rect x="6" y="6" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="9" width="6" height="6" rx="1" fill="currentColor" opacity=".18"/></svg>
                  {link["arch_display"]}
                </span>
                <strong>{link["readme_title"]}</strong>
              </div>
              <span class="date" data-date="{link["date"]}"></span>
            </a>
'''
            
            sections_html += '''          </div>
        </div>

'''
        
        sections_html += '''      </div>
    </section>

'''
    
    return sections_html

def main():
    """Main function to generate the HTML page."""
    try:
        print("Parsing README.md...")
        links = parse_readme_links()
        print(f"Found {len(links)} links")
        
        print("Grouping links by suite and Java version...")
        grouped_links = group_links_by_suite_and_java(links)
        
        print("Generating HTML...")
        html_content = generate_html(grouped_links)
        
        output_file = Path("new_page.html")
        output_file.write_text(html_content)
        
        print(f"Successfully generated {output_file}")
        
        # Print summary
        print("\nSummary:")
        for suite, java_versions in grouped_links.items():
            print(f"  {suite}:")
            for java_version, links in java_versions.items():
                print(f"    Java {java_version}: {len(links)} links")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
