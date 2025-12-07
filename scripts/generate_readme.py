#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime

def load_projects():
    projects = []
    projects_dir = Path('projects')
    for category_dir in projects_dir.iterdir():
        if category_dir.is_dir():
            for project_file in category_dir.glob('*.json'):
                with open(project_file, 'r', encoding='utf-8') as f:
                    project = json.load(f)
                    project['category'] = category_dir.name
                    projects.append(project)
    return projects

def generate_category_md(category, projects):
    category_emojis = {
        'web-applications': '🌐',
        'terminal-cli': '💻',
        'web-frameworks': '🛠️',
        'testing': '🧪',
        'os-lowlevel': '🖥️',
        'devops': '🔄',
        'text-processing': '📝',
        'networking': '🔒',
        'management': '🏢',
        'package-management': '📦',
        'dev-tools': '🔧',
        'mobile': '📱',
        'games': '🎮'
    }
    
    category_names = {
        'web-applications': 'Web Applications',
        'terminal-cli': 'Terminal & CLI',
        'web-frameworks': 'Web Frameworks & Tools',
        'testing': 'Testing & Automation',
        'os-lowlevel': 'Operating Systems & Low-Level',
        'devops': 'DevOps & System Administration',
        'text-processing': 'Text Processing & Analysis',
        'networking': 'VPN & Networking',
        'management': 'Management',
        'package-management': 'Package Management',
        'dev-tools': 'Development Tools',
        'mobile': 'Mobile Applications',
        'games': 'Games'
    }
    
    emoji = category_emojis.get(category, '📁')
    name = category_names.get(category, category.replace('-', ' ').title())
    
    category_projects = [p for p in projects if p.get('category') == category]
    if not category_projects:
        return ''
        
    # Explicit anchor so that TOC links like #(category) work
    # Wrap the whole category in a <details open> so it can be collapsed
    # Use inline <span> with larger font inside <summary>, so button и текст на одной строке
    md = [
        f'<h2 id="{category}"></h2>\n',
        f'<details open>\n',
        f'<summary><span style="font-size: 1.4em; font-weight: 600;">{emoji} {name}</span></summary>\n\n'
    ]
    
    for project in sorted(category_projects, key=lambda x: x['name'].lower()):
        # Project title and description as list item (project name bold)
        md.append(f"- **[{project['name']}]({project['url']})** - {project.get('description', '')}\n\n")
        
        # Details section, visually nested under the list item (like the example repo)
        md.append("  <details>\n")
        md.append("  <summary>Show details</summary>\n")
        md.append("  <p>\n\n")
        
        # Tech Stack
        if 'tech_stack' in project:
            md.append(f"  **Tech Stack**: {', '.join(project['tech_stack'])}\n\n")
            
        # Status
        if 'status' in project:
            md.append(f"  **Status**: {project['status']}\n\n")
            
        # Contribution
        if 'contribution' in project:
            md.append(f"  **Contribution**: {project['contribution']}\n\n")
            
        # # Maintainer
        # if 'maintainer' in project:
        #     maintainer = project['maintainer']
        #     if maintainer.startswith('@'):
        #         maintainer = f"[{maintainer}](https://github.com/{maintainer[1:]})"
        #     md.append(f"  **Maintainer**: {maintainer}\n\n")
            
        # Languages with icons
        # if 'languages' in project:
        #     lang_icons = {
        #         'go': 'golang',
        #         'typescript': 'typescript',
        #         'javascript': 'javascript',
        #         'python': 'python',
        #         'shell': 'shell',
        #         'c': 'c',
        #         'c++': 'cplusplus',
        #         'c#': 'csharp',
        #         'java': 'java',
        #         'php': 'php',
        #         'ruby': 'ruby',
        #         'rust': 'rust',
        #         'swift': 'swift',
        #         'kotlin': 'kotlin',
        #         'dart': 'dart',
        #         'r': 'r',
        #         'scala': 'scala',
        #         'haskell': 'haskell',
        #         'elixir': 'elixir',
        #         'clojure': 'clojure',
        #         'erlang': 'erlang',
        #         'ocaml': 'ocaml',
        #         'perl': 'perl',
        #         'r': 'r',
        #         'scala': 'scala',
        #         'swift': 'swift',
        #         'typescript': 'typescript',
        #         'vue': 'vue',
        #         'svelte': 'svelte',
        #         'angular': 'angular',
        #         'react': 'react',
        #         'nodejs': 'nodedotjs',
        #         'deno': 'deno',
        #         'docker': 'docker',
        #         'kubernetes': 'kubernetes',
        #         'terraform': 'terraform',
        #         'ansible': 'ansible',
        #         'bash': 'gnubash',
        #         'powershell': 'powershell',
        #         'html': 'html5',
        #         'css': 'css3',
        #         'sass': 'sass',
        #         'less': 'less',
        #         'graphql': 'graphql',
        #         'postgresql': 'postgresql',
        #         'mysql': 'mysql',
        #         'mongodb': 'mongodb',
        #         'redis': 'redis',
        #         'sqlite': 'sqlite'
        #     }
            
        #     languages = []
        #     for lang in project['languages']:
        #         icon_name = lang_icons.get(lang.lower().replace(' ', ''), '')
        #         if icon_name:
        #             languages.append(f"<img src='./icons/{lang.lower()}-16.png' alt='{lang}' height='16' loading='lazy'/> {lang}")
        #         else:
        #             languages.append(lang)
                    
        #     md.append(f"  **Languages**: {', '.join(languages)}\n\n")
        
        # Links
        if 'links' in project:
            link_items = []
            for name, url in project['links'].items():
                link_items.append(f"[{name}]({url})")
            md.append(f"  **Links**: {' | '.join(link_items)}\n\n")
            
        # Generate badges ONLY for GitHub projects (url contains github.com)
        badges = []
        if 'url' in project and 'github.com' in project['url'].lower():
            # Extract owner/repo from GitHub URL
            import re
            match = re.search(r'github\.com/([^/]+)/([^/]+)', project['url'].lower())
            if match:
                owner, repo = match.groups()
                if repo.endswith('.git'):
                    repo = repo[:-4]
                # Add standard GitHub badges
                badges.extend([
                    f"![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=flat-square&logo=github&label=Stars&cacheSeconds=3600)",
                    f"![GitHub license](https://img.shields.io/github/license/{owner}/{repo}?style=flat-square&cacheSeconds=86400)",
                    f"![GitHub last commit](https://img.shields.io/github/last-commit/{owner}/{repo}?style=flat-square&cacheSeconds=3600)",
                    f"![GitHub issues](https://img.shields.io/github/issues-raw/{owner}/{repo}?style=flat-square&cacheSeconds=3600)"
                ])
        
        if badges:
            md.append("  " + " ".join(badges) + "\n\n")
        
        # Image if exists
        if 'image' in project:
            md.append(f"  <img src='{project['image']}' width='600' loading='lazy' alt='{project['name']} Demo' style='margin-top: 10px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'/>\n\n")
        
        # Close paragraph and details, indented like in the example
        md.append("  </p>\n")
        md.append("  </details>\n\n")
    
    # Close category details block and add small separator between categories
    md.append('</details>\n\n<hr />\n')
    
    return '\n'.join(md)

def generate_readme(projects):
    # Load template
    with open('templates/README.template.md', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate categories
    categories = sorted(list(set(p['category'] for p in projects)))

    # Custom desired order for categories in Contents / layout
    preferred_order = [
        'terminal-cli',
        'web-applications',
        'web-frameworks',
        'devops',
        'operating-systems',
        'management',
        'package-management',
        'testing',
        'text-processing',
        'vpn',
    ]

    ordered_categories = [c for c in preferred_order if c in categories]
    # Append any categories not explicitly ordered (e.g. dev-tools, mobile, games)
    ordered_categories.extend(c for c in categories if c not in preferred_order)
    
    # Generate TOC
    category_links = []
    for category in ordered_categories:
        name = category.replace('-', ' ').title()
        if category == 'web-frameworks':
            name = 'Web Frameworks & Tools'
        elif category == 'terminal-cli':
            name = 'Terminal & CLI'
        elif category == 'os-lowlevel':
            name = 'Operating Systems & Low-Level'
        elif category == 'text-processing':
            name = 'Text Processing & Analysis'
        elif category == 'networking':
            name = 'VPN & Networking'
        elif category == 'dev-tools':
            name = 'Development Tools'
        elif category == 'mobile':
            name = 'Mobile Applications'
        category_links.append(f"- [{name}](#{category})")
    
    # Generate content for each category (in the same ordered sequence)
    category_contents = []
    for category in ordered_categories:
        content = generate_category_md(category, projects)
        if content:
            category_contents.append(content)
    
    # Replace placeholders
    readme = template
    readme = readme.replace('{{LAST_UPDATED}}', datetime.now().strftime('%B %d, %Y'))
    readme = readme.replace('{{TOTAL_PROJECTS}}', str(len(projects)))
    readme = readme.replace('{{TOTAL_CATEGORIES}}', str(len(categories)))
    readme = readme.replace('{{CATEGORY_LINKS}}', '\n'.join(category_links))
    readme = readme.replace('{{CATEGORY_CONTENT}}', '\n'.join(category_contents))
    
    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)

def main():
    projects = load_projects()
    generate_readme(projects)
    print("README.md generated successfully!")

if __name__ == "__main__":
    main()
