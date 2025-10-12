# Complete Portfolio CMS - Static Site Generator
# Install: pip install flask python-dotenv

import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')

# Configuration
OUTPUT_DIR = 'public'
DATA_FILE = 'site_data.json'
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Create directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'blog'), exist_ok=True)

# Initialize data file with default content
DEFAULT_DATA = {
    'site_info': {
        'name': 'Mamdhooh Moomin Rasheed',
        'title': 'Pentester & Developer',
        'description': 'Penetration tester and developer with a lifelong passion for breaking systems to build them better.',
        'email': 'contact@mamdhooh.com',
        'twitter': '@moominrasheed',
        'domain': 'mamdhooh.com'
    },
    'hero': {
        'tag': '🛡️ Security · Development · Innovation',
        'title': 'Mamdhooh Moomin Rasheed',
        'description': 'Penetration tester and developer with a lifelong passion for breaking systems to build them better. I find vulnerabilities, write code, and secure the digital world one exploit at a time.'
    },
    'footer': {
        'text': '© 2025 Mamdhooh Moomin Rasheed. Built for speed and security.',
        'tagline': 'root@mamdhooh:~$ whoami'
    },
    'expertise': [
        {
            'icon': '🔒',
            'title': 'Penetration Testing',
            'description': 'Comprehensive security assessments, vulnerability research, and exploit development. I think like an attacker to defend like a pro.'
        },
        {
            'icon': '💻',
            'title': 'Full-Stack Development',
            'description': 'Building secure, scalable applications from frontend to backend. Security-first development is not just a practice, it\'s a mindset.'
        },
        {
            'icon': '🔍',
            'title': 'Security Research',
            'description': 'Discovering zero-days, analyzing attack vectors, and contributing to the security community with responsible disclosure.'
        },
        {
            'icon': '⚡',
            'title': 'DevSecOps',
            'description': 'Integrating security into every stage of development. Automation, CI/CD pipelines, and security tooling that scales.'
        },
        {
            'icon': '🎯',
            'title': 'Red Team Operations',
            'description': 'Simulating real-world attacks to test defenses. Social engineering, network penetration, and physical security assessments.'
        },
        {
            'icon': '🛠️',
            'title': 'Tool Development',
            'description': 'Creating custom security tools and automation scripts. If it doesn\'t exist, I\'ll build it myself.'
        }
    ],
    'skills': [
        'Python', 'JavaScript', 'Go', 'Bash', 'React', 'Node.js',
        'Burp Suite', 'Metasploit', 'Nmap', 'Wireshark', 'Docker',
        'Kubernetes', 'AWS', 'Linux', 'OWASP', 'Web Application Security',
        'Network Security', 'Reverse Engineering', 'Binary Exploitation', 'API Security'
    ],
    'posts': []
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump(DEFAULT_DATA, f, indent=2)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Load/Save data
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Base CSS (minified for speed)
BASE_CSS = '''*{margin:0;padding:0;box-sizing:border-box}:root{--bg:#0a0a0a;--card:#1a1a1a;--text:#fff;--text-dim:#a0a0a0;--accent:#00ff88;--border:#2a2a2a}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.grid-bg{position:fixed;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(var(--accent) 1px,transparent 1px),linear-gradient(90deg,var(--accent) 1px,transparent 1px);background-size:50px 50px;opacity:.03;pointer-events:none;animation:grid 20s linear infinite}
@keyframes grid{0%{transform:translate(0,0)}100%{transform:translate(50px,50px)}}
nav{position:fixed;top:0;width:100%;background:rgba(10,10,10,.8);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);z-index:1000;padding:1.5rem 2rem}
.nav-content{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:1.5rem;font-weight:700;color:var(--accent);letter-spacing:-.5px;text-decoration:none}
.nav-links{display:flex;gap:2rem;list-style:none}
.nav-links a{color:var(--text-dim);text-decoration:none;font-weight:500;transition:color .3s}
.nav-links a:hover{color:var(--accent)}
.container{max-width:1400px;margin:0 auto;padding:0 2rem;position:relative;z-index:1}
.hero{min-height:100vh;display:flex;align-items:center;padding-top:80px}
.hero-tag{display:inline-block;padding:.5rem 1rem;background:rgba(0,255,136,.1);border:1px solid var(--accent);border-radius:50px;color:var(--accent);font-size:.9rem;font-weight:600;margin-bottom:2rem}
h1{font-size:clamp(3rem,8vw,6rem);font-weight:800;line-height:1.1;margin-bottom:1.5rem;background:linear-gradient(135deg,#fff 0%,var(--accent) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-description{font-size:1.3rem;color:var(--text-dim);margin-bottom:3rem;line-height:1.8}
.cta-buttons{display:flex;gap:1rem;flex-wrap:wrap}
.btn{padding:1rem 2rem;border-radius:12px;text-decoration:none;font-weight:600;transition:all .3s;display:inline-flex;align-items:center;gap:.5rem}
.btn-primary{background:var(--accent);color:var(--bg);border:2px solid var(--accent)}
.btn-primary:hover{background:transparent;color:var(--accent);transform:translateY(-2px);box-shadow:0 10px 40px rgba(0,255,136,.3)}
.btn-secondary{background:transparent;color:var(--text);border:2px solid var(--border)}
.btn-secondary:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px)}
section{padding:8rem 0}
.section-header{text-align:center;margin-bottom:5rem}
.section-tag{color:var(--accent);font-weight:600;font-size:.9rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem}
h2{font-size:clamp(2.5rem,5vw,4rem);font-weight:800;margin-bottom:1rem}
.section-description{font-size:1.2rem;color:var(--text-dim);max-width:600px;margin:0 auto}
.expertise-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem}
.expertise-card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:2.5rem;transition:all .3s}
.expertise-card:hover{transform:translateY(-5px);border-color:var(--accent);box-shadow:0 20px 60px rgba(0,255,136,.1)}
.expertise-icon{font-size:3rem;margin-bottom:1.5rem}
.expertise-card h3{font-size:1.5rem;margin-bottom:1rem}
.expertise-card p{color:var(--text-dim);line-height:1.8}
.skills-container{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;max-width:900px;margin:0 auto}
.skill-tag{padding:.8rem 1.5rem;background:var(--card);border:1px solid var(--border);border-radius:50px;font-weight:500;transition:all .3s}
.skill-tag:hover{background:rgba(0,255,136,.1);border-color:var(--accent);color:var(--accent);transform:translateY(-2px)}
.blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:2rem}
.blog-card{background:var(--card);border:1px solid var(--border);border-radius:20px;overflow:hidden;transition:all .3s;text-decoration:none;color:inherit;display:block}
.blog-card:hover{transform:translateY(-8px);border-color:var(--accent);box-shadow:0 20px 60px rgba(0,255,136,.15)}
.blog-image{height:200px;background:linear-gradient(135deg,#1a1a1a 0%,#2a2a2a 100%);display:flex;align-items:center;justify-content:center;font-size:4rem;border-bottom:1px solid var(--border)}
.blog-content{padding:2rem}
.blog-meta{display:flex;gap:1rem;margin-bottom:1rem;font-size:.85rem;color:var(--text-dim)}
.blog-tag-small{color:var(--accent);font-weight:600}
.blog-card h3{font-size:1.4rem;margin-bottom:.8rem;line-height:1.3}
.blog-excerpt{color:var(--text-dim);line-height:1.7;margin-bottom:1.5rem}
.read-more{color:var(--accent);font-weight:600;display:inline-flex;align-items:center;gap:.5rem}
.contact-content{max-width:700px;margin:0 auto;text-align:center}
.contact-links{display:flex;gap:1.5rem;justify-content:center;flex-wrap:wrap;margin-top:3rem}
.contact-link{display:flex;align-items:center;gap:.8rem;padding:1.2rem 2rem;background:var(--card);border:1px solid var(--border);border-radius:15px;color:var(--text);text-decoration:none;font-weight:600;transition:all .3s}
.contact-link:hover{border-color:var(--accent);background:rgba(0,255,136,.05);transform:translateY(-3px);box-shadow:0 10px 40px rgba(0,255,136,.2)}
footer{border-top:1px solid var(--border);padding:3rem 0;text-align:center;color:var(--text-dim)}
.terminal{font-family:'Courier New',monospace;color:var(--accent);margin-bottom:1rem}
.article{padding:10rem 0 5rem}
.back-link{display:inline-flex;align-items:center;gap:.5rem;color:var(--text-dim);text-decoration:none;margin-bottom:3rem;transition:color .3s}
.back-link:hover{color:var(--accent)}
.article-icon{font-size:5rem;margin-bottom:2rem}
.article-meta{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:2rem;font-size:.9rem;color:var(--text-dim)}
.article-category{color:var(--accent);font-weight:600}
.article-content{font-size:1.1rem;line-height:1.9}
.article-content h2{font-size:2rem;margin:3rem 0 1rem;color:var(--accent)}
.article-content h3{font-size:1.5rem;margin:2rem 0 1rem}
.article-content p{margin:1.5rem 0;color:var(--text-dim)}
.article-content ul,.article-content ol{margin:1.5rem 0;padding-left:2rem}
.article-content li{margin:.5rem 0;color:var(--text-dim)}
.article-content code{background:var(--card);padding:.2rem .5rem;border-radius:4px;color:var(--accent);font-family:'Courier New',monospace}
.article-content pre{background:var(--card);padding:1.5rem;border-radius:8px;overflow-x:auto;margin:1.5rem 0;border:1px solid var(--border)}
.article-content pre code{background:none;padding:0}
.article-content blockquote{border-left:4px solid var(--accent);padding-left:1.5rem;margin:1.5rem 0;font-style:italic;color:var(--text-dim)}
@media(max-width:768px){nav{padding:1rem}.nav-links{gap:1rem;font-size:.9rem}section{padding:4rem 0}.expertise-grid,.blog-grid{grid-template-columns:1fr}.contact-links{flex-direction:column}}'''

# HTML Templates
def generate_index_html(data):
    # Get only the first published post for homepage
    published_posts = [p for p in data['posts'] if p.get('published', True)]
    featured_post = published_posts[0] if published_posts else None
    
    featured_blog = ''
    if featured_post:
        featured_blog = f'''
        <section id="blog">
            <div class="section-header">
                <div class="section-tag">Latest Insight</div>
                <h2>Featured Post</h2>
            </div>
            <div style="max-width:800px;margin:0 auto">
                <a href="blog/{featured_post["slug"]}.html" class="blog-card">
                    <div class="blog-image">{featured_post["icon"]}</div>
                    <div class="blog-content">
                        <div class="blog-meta">
                            <span class="blog-tag-small">{featured_post["category"]}</span>
                            <span>•</span>
                            <span>{featured_post["date"]}</span>
                            <span>•</span>
                            <span>{featured_post["read_time"]}</span>
                        </div>
                        <h3>{featured_post["title"]}</h3>
                        <p class="blog-excerpt">{featured_post["excerpt"]}</p>
                        <span class="read-more">Read More →</span>
                    </div>
                </a>
                <div style="text-align:center;margin-top:2rem">
                    <a href="blog.html" class="btn btn-secondary">View All Posts →</a>
                </div>
            </div>
        </section>'''
    
    expertise_cards = ''
    for item in data['expertise']:
        expertise_cards += f'''
                <div class="expertise-card">
                    <div class="expertise-icon">{item["icon"]}</div>
                    <h3>{item["title"]}</h3>
                    <p>{item["description"]}</p>
                </div>'''
    
    skills_tags = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in data['skills']])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["site_info"]["name"]} - {data["site_info"]["title"]}</title>
    <meta name="description" content="{data["site_info"]["description"]}">
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="grid-bg"></div>
    
    <nav>
        <div class="nav-content">
            <a href="index.html" class="logo">MR.</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#expertise">Expertise</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <section class="hero" id="home">
            <div class="hero-content">
                <div class="hero-tag">{data["hero"]["tag"]}</div>
                <h1>{data["hero"]["title"]}</h1>
                <p class="hero-description">{data["hero"]["description"]}</p>
                <div class="cta-buttons">
                    <a href="#contact" class="btn btn-primary">Get in Touch<span>→</span></a>
                    <a href="https://x.com/{data["site_info"]["twitter"][1:]}" target="_blank" class="btn btn-secondary">Follow on X</a>
                </div>
            </div>
        </section>

        <section id="expertise">
            <div class="section-header">
                <div class="section-tag">What I Do</div>
                <h2>Expertise</h2>
                <p class="section-description">Bridging the gap between security and development with deep technical knowledge</p>
            </div>
            <div class="expertise-grid">{expertise_cards}</div>
        </section>

        <section id="skills">
            <div class="section-header">
                <div class="section-tag">Tech Stack</div>
                <h2>Skills & Tools</h2>
            </div>
            <div class="skills-container">{skills_tags}</div>
        </section>

        {featured_blog}

        <section id="contact">
            <div class="contact-content">
                <div class="section-header">
                    <div class="section-tag">Let's Connect</div>
                    <h2>Get in Touch</h2>
                    <p class="section-description">Whether it's a security consultation, collaboration opportunity, or just a chat about the latest CVE</p>
                </div>
                <div class="contact-links">
                    <a href="https://x.com/{data["site_info"]["twitter"][1:]}" target="_blank" class="contact-link"><span>𝕏</span><span>{data["site_info"]["twitter"]}</span></a>
                    <a href="mailto:{data["site_info"]["email"]}" class="contact-link"><span>✉️</span><span>{data["site_info"]["email"]}</span></a>
                </div>
            </div>
        </section>
    </div>

    <footer>
        <div class="container">
            <p class="terminal">{data["footer"]["tagline"]}</p>
            <p>{data["footer"]["text"]}</p>
        </div>
    </footer>
</body>
</html>'''

def generate_blog_page_html(data):
    """Generate the main blog listing page"""
    blog_cards = ''
    for post in [p for p in data['posts'] if p.get('published', True)]:
        blog_cards += f'''
                <a href="blog/{post["slug"]}.html" class="blog-card">
                    <div class="blog-image">{post["icon"]}</div>
                    <div class="blog-content">
                        <div class="blog-meta">
                            <span class="blog-tag-small">{post["category"]}</span>
                            <span>•</span>
                            <span>{post["date"]}</span>
                            <span>•</span>
                            <span>{post["read_time"]}</span>
                        </div>
                        <h3>{post["title"]}</h3>
                        <p class="blog-excerpt">{post["excerpt"]}</p>
                        <span class="read-more">Read More →</span>
                    </div>
                </a>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - {data["site_info"]["name"]}</title>
    <meta name="description" content="Security insights, development tips, and penetration testing techniques">
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="grid-bg"></div>
    
    <nav>
        <div class="nav-content">
            <a href="index.html" class="logo">MR.</a>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="index.html#expertise">Expertise</a></li>
                <li><a href="index.html#skills">Skills</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="index.html#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <div class="container" style="padding-top:120px">
        <section style="padding:4rem 0">
            <div class="section-header">
                <div class="section-tag">Latest Insights</div>
                <h2>All Blog Posts</h2>
                <p class="section-description">Thoughts on security, development, and breaking things the right way</p>
            </div>
            <div class="blog-grid">{blog_cards}</div>
        </section>
    </div>

    <footer>
        <div class="container">
            <p class="terminal">{data["footer"]["tagline"]}</p>
            <p>{data["footer"]["text"]}</p>
        </div>
    </footer>
</body>
</html>'''

def generate_post_html(post, site_info, footer):
    content_html = markdown_to_html(post['content'])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post["title"]} - {site_info["name"]}</title>
    <meta name="description" content="{post["excerpt"]}">
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="grid-bg"></div>
    
    <nav>
        <div class="nav-content">
            <a href="../index.html" class="logo">MR.</a>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <article class="article">
            <a href="../index.html#blog" class="back-link">← Back to Blog</a>
            <div class="article-icon">{post["icon"]}</div>
            <div class="article-meta">
                <span class="article-category">{post["category"]}</span>
                <span>•</span>
                <span>{post["date"]}</span>
                <span>•</span>
                <span>{post["read_time"]}</span>
            </div>
            <h1>{post["title"]}</h1>
            <div class="article-content">{content_html}</div>
        </article>
    </div>

    <footer>
        <div class="container">
            <p>© 2025 {site_info["name"]}</p>
        </div>
    </footer>
</body>
</html>'''

def markdown_to_html(text):
    """Simple markdown to HTML converter"""
    html = ''
    lines = text.split('\n')
    in_code_block = False
    in_list = False
    code_block = ''
    list_type = ''
    
    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html += f'<pre><code>{code_block.strip()}</code></pre>'
                code_block = ''
                in_code_block = False
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_block += line + '\n'
            continue
        
        # Headers
        if line.startswith('# '):
            if in_list:
                html += f'</{list_type}>'
                in_list = False
            html += f'<h2>{line[2:]}</h2>'
        elif line.startswith('## '):
            if in_list:
                html += f'</{list_type}>'
                in_list = False
            html += f'<h2>{line[3:]}</h2>'
        elif line.startswith('### '):
            if in_list:
                html += f'</{list_type}>'
                in_list = False
            html += f'<h3>{line[4:]}</h3>'
        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html += '<ul>'
                in_list = True
                list_type = 'ul'
            html += f'<li>{line.strip()[2:]}</li>'
        elif line.strip() and line.strip()[0].isdigit() and '. ' in line:
            if not in_list:
                html += '<ol>'
                in_list = True
                list_type = 'ol'
            html += f'<li>{line.strip().split(".", 1)[1].strip()}</li>'
        # Blockquote
        elif line.strip().startswith('>'):
            if in_list:
                html += f'</{list_type}>'
                in_list = False
            html += f'<blockquote>{line.strip()[1:].strip()}</blockquote>'
        # Paragraph
        elif line.strip():
            if in_list:
                html += f'</{list_type}>'
                in_list = False
            # Bold
            while '**' in line:
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
            # Italic
            while '_' in line and line.count('_') >= 2:
                line = line.replace('_', '<em>', 1).replace('_', '</em>', 1)
            # Inline code
            while '`' in line and line.count('`') >= 2:
                line = line.replace('`', '<code>', 1).replace('`', '</code>', 1)
            html += f'<p>{line}</p>'
        else:
            if in_list:
                html += f'</{list_type}>'
                in_list = False
    
    if in_list:
        html += f'</{list_type}>'
    
    return html

def create_slug(title):
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
    slug = '-'.join(slug.split())
    return slug

def generate_site():
    """Generate all static HTML files"""
    data = load_data()
    
    # Generate index.html
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(generate_index_html(data))
    
    # Generate blog.html (all posts page)
    with open(os.path.join(OUTPUT_DIR, 'blog.html'), 'w', encoding='utf-8') as f:
        f.write(generate_blog_page_html(data))
    
    # Generate individual blog posts
    for post in [p for p in data['posts'] if p.get('published', True)]:
        post_html = generate_post_html(post, data['site_info'], data['footer'])
        with open(os.path.join(OUTPUT_DIR, 'blog', f"{post['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(post_html)

# Admin Templates
ADMIN_CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0a;color:#fff;line-height:1.6;padding:2rem}
.container{max-width:1200px;margin:0 auto}h1,h2{color:#00ff88;margin-bottom:1.5rem}
.btn{padding:.8rem 1.5rem;background:#00ff88;color:#0a0a0a;border:none;border-radius:8px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-block;margin:.5rem;transition:background .3s}
.btn:hover{background:#00cc6a}.btn-danger{background:#ff4444}.btn-danger:hover{background:#cc0000}
.btn-secondary{background:#666}.btn-secondary:hover{background:#555}
.card{background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1rem}
.form-group{margin-bottom:1.5rem}label{display:block;margin-bottom:.5rem;color:#00ff88;font-weight:600}
input,textarea,select{width:100%;padding:.8rem;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;color:#fff;font-family:inherit;font-size:1rem}
textarea{min-height:100px;font-family:'Courier New',monospace}.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.success{background:#00ff88;color:#0a0a0a;padding:1rem;border-radius:8px;margin-bottom:1rem;font-weight:600}
.tabs{display:flex;gap:1rem;margin-bottom:2rem;border-bottom:2px solid #2a2a2a}
.tab{padding:1rem 2rem;cursor:pointer;border-bottom:2px solid transparent;transition:all .3s}
.tab.active{border-bottom-color:#00ff88;color:#00ff88}
.tab:hover{color:#00ff88}
.item-list{display:grid;gap:1rem}.item{display:flex;justify-content:space-between;align-items:center}
.item-info{flex:1}.item-actions{display:flex;gap:.5rem}
table{width:100%;border-collapse:collapse}th,td{padding:1rem;text-align:left;border-bottom:1px solid #2a2a2a}
th{color:#00ff88;font-weight:600}
.nav-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem}'''

ADMIN_LOGIN = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Login</title><style>''' + ADMIN_CSS + '''
.login-container{max-width:400px;margin:10vh auto}</style></head>
<body><div class="login-container"><div class="card">
<h1 style="text-align:center">🔐 Admin Login</h1>
{% if error %}<div style="background:#ff4444;color:#fff;padding:1rem;border-radius:8px;margin-bottom:1rem">{{ error }}</div>{% endif %}
<form method="POST">
<div class="form-group"><label>Username</label><input type="text" name="username" required autofocus></div>
<div class="form-group"><label>Password</label><input type="password" name="password" required></div>
<button type="submit" class="btn" style="width:100%">Login</button>
</form></div></div></body></html>'''

ADMIN_DASHBOARD = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CMS Dashboard</title><style>''' + ADMIN_CSS + '''</style></head>
<body><div class="container">
<div class="nav-top"><h1>🎨 Portfolio CMS</h1><a href="/admin/logout" class="btn btn-danger">Logout</a></div>
{% if message %}<div class="success">{{ message }}</div>{% endif %}
<div class="tabs">
<div class="tab {% if tab == 'site' %}active{% endif %}" onclick="location.href='/admin?tab=site'">Site Settings</div>
<div class="tab {% if tab == 'content' %}active{% endif %}" onclick="location.href='/admin?tab=content'">Content</div>
<div class="tab {% if tab == 'blog' %}active{% endif %}" onclick="location.href='/admin?tab=blog'">Blog Posts</div>
</div>

{% if tab == 'site' %}
<h2>Site Settings</h2>
<form method="POST" action="/admin/save-site-info">
<div class="card">
<div class="grid-2">
<div class="form-group"><label>Name</label><input type="text" name="name" value="{{ site_info.name }}" required></div>
<div class="form-group"><label>Title</label><input type="text" name="title" value="{{ site_info.title }}" required></div>
</div>
<div class="form-group"><label>Description</label><textarea name="description" rows="3" required>{{ site_info.description }}</textarea></div>
<div class="grid-2">
<div class="form-group"><label>Email</label><input type="email" name="email" value="{{ site_info.email }}" required></div>
<div class="form-group"><label>Twitter</label><input type="text" name="twitter" value="{{ site_info.twitter }}" required></div>
</div>
<button type="submit" class="btn">💾 Save Site Settings</button>
</div>
</form>

<h2>Hero Section</h2>
<form method="POST" action="/admin/save-hero">
<div class="card">
<div class="form-group"><label>Tag Line</label><input type="text" name="tag" value="{{ hero.tag }}" required></div>
<div class="form-group"><label>Hero Title</label><input type="text" name="title" value="{{ hero.title }}" required></div>
<div class="form-group"><label>Description</label><textarea name="description" rows="4" required>{{ hero.description }}</textarea></div>
<button type="submit" class="btn">💾 Save Hero Section</button>
</div>
</form>

<h2>Footer</h2>
<form method="POST" action="/admin/save-footer">
<div class="card">
<div class="form-group"><label>Terminal Tagline</label><input type="text" name="tagline" value="{{ footer.tagline }}" required></div>
<div class="form-group"><label>Footer Text</label><input type="text" name="text" value="{{ footer.text }}" required></div>
<button type="submit" class="btn">💾 Save Footer</button>
</div>
</form>
{% endif %}

{% if tab == 'content' %}
<div style="display:flex;justify-content:space-between;align-items:center">
<h2>Expertise Cards</h2>
<a href="/admin/add-expertise" class="btn">+ Add Expertise</a>
</div>
<div class="item-list">
{% for exp in expertise %}
<div class="card item">
<div class="item-info">
<h3>{{ exp.icon }} {{ exp.title }}</h3>
<p style="color:#a0a0a0">{{ exp.description[:100] }}...</p>
</div>
<div class="item-actions">
<a href="/admin/edit-expertise/{{ loop.index0 }}" class="btn btn-secondary">Edit</a>
<a href="/admin/delete-expertise/{{ loop.index0 }}" class="btn btn-danger" onclick="return confirm('Delete?')">Delete</a>
</div>
</div>
{% endfor %}
</div>

<h2 style="margin-top:3rem">Skills</h2>
<form method="POST" action="/admin/save-skills">
<div class="card">
<div class="form-group">
<label>Skills (comma-separated)</label>
<textarea name="skills" rows="5" required>{{ skills|join(', ') }}</textarea>
</div>
<button type="submit" class="btn">💾 Save Skills</button>
</div>
</form>
{% endif %}

{% if tab == 'blog' %}
<div style="display:flex;justify-content:space-between;align-items:center">
<h2>Blog Posts ({{ posts|length }})</h2>
<div>
<a href="/admin/regenerate" class="btn btn-secondary">🔄 Regenerate Site</a>
<a href="/admin/new-post" class="btn">+ New Post</a>
</div>
</div>
<div class="item-list">
{% for post in posts %}
<div class="card item">
<div style="display:flex;align-items:center;gap:1rem;flex:1">
<span style="font-size:2rem">{{ post.icon }}</span>
<div class="item-info">
<h3>{{ post.title }}</h3>
<p style="color:#a0a0a0">{{ post.category }} • {{ post.date }} • {% if post.published %}Published{% else %}Draft{% endif %}</p>
</div>
</div>
<div class="item-actions">
<a href="/admin/edit-post/{{ post.id }}" class="btn btn-secondary">Edit</a>
<a href="/admin/delete-post/{{ post.id }}" class="btn btn-danger" onclick="return confirm('Delete?')">Delete</a>
</div>
</div>
{% endfor %}
</div>
{% endif %}

</div></body></html>'''

ADMIN_EDIT_EXPERTISE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% if expertise %}Edit{% else %}Add{% endif %} Expertise</title><style>''' + ADMIN_CSS + '''</style></head>
<body><div class="container">
<a href="/admin?tab=content" style="color:#00ff88;text-decoration:none">← Back to Content</a>
<h1>{% if expertise %}Edit{% else %}Add{% endif %} Expertise</h1>
<form method="POST">
<div class="card">
<div class="form-group">
<label>Icon (emoji)</label>
<input type="text" name="icon" value="{% if expertise %}{{ expertise.icon }}{% endif %}" required>
</div>
<div class="form-group">
<label>Title</label>
<input type="text" name="title" value="{% if expertise %}{{ expertise.title }}{% endif %}" required>
</div>
<div class="form-group">
<label>Description</label>
<textarea name="description" rows="5" required>{% if expertise %}{{ expertise.description }}{% endif %}</textarea>
</div>
<button type="submit" class="btn">💾 Save</button>
<a href="/admin?tab=content" class="btn btn-secondary">Cancel</a>
</div>
</form>
</div></body></html>'''

ADMIN_EDIT_POST = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% if post %}Edit{% else %}New{% endif %} Post</title><style>''' + ADMIN_CSS + '''textarea{min-height:400px}</style></head>
<body><div class="container">
<a href="/admin?tab=blog" style="color:#00ff88;text-decoration:none">← Back to Blog</a>
<h1>{% if post %}Edit Post{% else %}New Post{% endif %}</h1>
<form method="POST">
<div class="card">
<div class="grid-2">
<div class="form-group">
<label>Icon</label>
<select name="icon" required>
<option value="🔐" {% if post and post.icon == '🔐' %}selected{% endif %}>🔐 Security</option>
<option value="💻" {% if post and post.icon == '💻' %}selected{% endif %}>💻 Development</option>
<option value="🎯" {% if post and post.icon == '🎯' %}selected{% endif %}>🎯 Red Team</option>
<option value="🛠️" {% if post and post.icon == '🛠️' %}selected{% endif %}>🛠️ Tools</option>
<option value="🔍" {% if post and post.icon == '🔍' %}selected{% endif %}>🔍 Research</option>
<option value="⚡" {% if post and post.icon == '⚡' %}selected{% endif %}>⚡ DevSecOps</option>
<option value="🚀" {% if post and post.icon == '🚀' %}selected{% endif %}>🚀 Other</option>
</select>
</div>
<div class="form-group">
<label>Category</label>
<select name="category" required>
<option value="SECURITY" {% if post and post.category == 'SECURITY' %}selected{% endif %}>Security</option>
<option value="DEVELOPMENT" {% if post and post.category == 'DEVELOPMENT' %}selected{% endif %}>Development</option>
<option value="RED TEAM" {% if post and post.category == 'RED TEAM' %}selected{% endif %}>Red Team</option>
<option value="TOOLS" {% if post and post.category == 'TOOLS' %}selected{% endif %}>Tools</option>
<option value="RESEARCH" {% if post and post.category == 'RESEARCH' %}selected{% endif %}>Research</option>
<option value="DEVSECOPS" {% if post and post.category == 'DEVSECOPS' %}selected{% endif %}>DevSecOps</option>
</select>
</div>
</div>
<div class="form-group">
<label>Title</label>
<input type="text" name="title" value="{% if post %}{{ post.title }}{% endif %}" required>
</div>
<div class="form-group">
<label>Excerpt</label>
<textarea name="excerpt" rows="2" required>{% if post %}{{ post.excerpt }}{% endif %}</textarea>
</div>
<div class="form-group">
<label>Content (Markdown)</label>
<textarea name="content" required>{% if post %}{{ post.content }}{% endif %}</textarea>
<small style="color:#a0a0a0">Use # for headers, ** for bold, - for lists, ``` for code blocks</small>
</div>
<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
<input type="checkbox" name="published" id="published" {% if not post or post.published %}checked{% endif %}>
<label for="published" style="margin:0">Published</label>
</div>
<button type="submit" class="btn">💾 Save Post</button>
<a href="/admin?tab=blog" class="btn btn-secondary">Cancel</a>
</div>
</form>
</div></body></html>'''

# Routes
@app.route('/')
def index():
    return '''<html><head><title>Portfolio CMS</title><style>body{font-family:sans-serif;max-width:800px;margin:50px auto;padding:20px;background:#0a0a0a;color:#fff}
h1{color:#00ff88}a{color:#00ff88;text-decoration:none;padding:10px 20px;background:#1a1a1a;border-radius:8px;display:inline-block;margin-top:20px}
a:hover{background:#2a2a2a}ul{line-height:2}</style></head><body>
<h1>🚀 Portfolio CMS - Running!</h1>
<p>Your static site generator is ready. The site is generated in the <code>public/</code> directory.</p>
<h2>Quick Start:</h2>
<ul>
<li>Open <a href="/admin">/admin</a> to manage your portfolio (default: admin/admin123)</li>
<li>Edit site info, content, expertise, skills, and blog posts</li>
<li>Every save automatically regenerates static HTML files</li>
<li>Deploy the <code>public/</code> folder anywhere!</li>
</ul>
<h2>Features:</h2>
<ul>
<li>✅ Manage everything: site settings, hero, expertise, skills, blog</li>
<li>✅ Pure HTML output - ultra fast loading</li>
<li>✅ No JavaScript framework on frontend</li>
<li>✅ Markdown support for blog posts</li>
<li>✅ Auto-regeneration on every change</li>
<li>✅ SEO-friendly static pages</li>
</ul>
<a href="/admin">Open Admin Panel →</a>
<a href="public/index.html" target="_blank">View Site →</a>
</body></html>'''

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template_string(ADMIN_LOGIN, error='Invalid credentials')
    
    return render_template_string(ADMIN_LOGIN)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    data = load_data()
    tab = request.args.get('tab', 'site')
    message = request.args.get('message')
    
    posts = sorted(data['posts'], key=lambda x: x.get('date', ''), reverse=True)
    
    return render_template_string(
        ADMIN_DASHBOARD,
        tab=tab,
        message=message,
        site_info=data['site_info'],
        hero=data['hero'],
        footer=data['footer'],
        expertise=data['expertise'],
        skills=data['skills'],
        posts=posts
    )

@app.route('/admin/save-site-info', methods=['POST'])
@login_required
def save_site_info():
    data = load_data()
    data['site_info'] = {
        'name': request.form.get('name'),
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'email': request.form.get('email'),
        'twitter': request.form.get('twitter'),
        'domain': data['site_info'].get('domain', 'mamdhooh.com')
    }
    save_data(data)
    generate_site()
    return redirect(url_for('admin_dashboard', tab='site', message='Site settings saved!'))

@app.route('/admin/save-hero', methods=['POST'])
@login_required
def save_hero():
    data = load_data()
    data['hero'] = {
        'tag': request.form.get('tag'),
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    save_data(data)
    generate_site()
    return redirect(url_for('admin_dashboard', tab='site', message='Hero section saved!'))

@app.route('/admin/save-footer', methods=['POST'])
@login_required
def save_footer():
    data = load_data()
    data['footer'] = {
        'tagline': request.form.get('tagline'),
        'text': request.form.get('text')
    }
    save_data(data)
    generate_site()
    return redirect(url_for('admin_dashboard', tab='site', message='Footer saved!'))

@app.route('/admin/save-skills', methods=['POST'])
@login_required
def save_skills():
    data = load_data()
    skills_text = request.form.get('skills')
    data['skills'] = [s.strip() for s in skills_text.split(',') if s.strip()]
    save_data(data)
    generate_site()
    return redirect(url_for('admin_dashboard', tab='content', message='Skills saved!'))

@app.route('/admin/add-expertise', methods=['GET', 'POST'])
@login_required
def add_expertise():
    if request.method == 'POST':
        data = load_data()
        new_exp = {
            'icon': request.form.get('icon'),
            'title': request.form.get('title'),
            'description': request.form.get('description')
        }
        data['expertise'].append(new_exp)
        save_data(data)
        generate_site()
        return redirect(url_for('admin_dashboard', tab='content', message='Expertise added!'))
    
    return render_template_string(ADMIN_EDIT_EXPERTISE, expertise=None)

@app.route('/admin/edit-expertise/<int:idx>', methods=['GET', 'POST'])
@login_required
def edit_expertise(idx):
    data = load_data()
    
    if request.method == 'POST':
        data['expertise'][idx] = {
            'icon': request.form.get('icon'),
            'title': request.form.get('title'),
            'description': request.form.get('description')
        }
        save_data(data)
        generate_site()
        return redirect(url_for('admin_dashboard', tab='content', message='Expertise updated!'))
    
    return render_template_string(ADMIN_EDIT_EXPERTISE, expertise=data['expertise'][idx])

@app.route('/admin/delete-expertise/<int:idx>')
@login_required
def delete_expertise(idx):
    data = load_data()
    data['expertise'].pop(idx)
    save_data(data)
    generate_site()
    return redirect(url_for('admin_dashboard', tab='content', message='Expertise deleted!'))

@app.route('/admin/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        data = load_data()
        title = request.form.get('title')
        content = request.form.get('content')
        word_count = len(content.split())
        read_time = f"{max(1, word_count // 200)} min"
        
        new_post = {
            'id': max([p['id'] for p in data['posts']], default=0) + 1,
            'title': title,
            'slug': create_slug(title),
            'excerpt': request.form.get('excerpt'),
            'content': content,
            'category': request.form.get('category'),
            'icon': request.form.get('icon'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'read_time': read_time,
            'published': 'published' in request.form
        }
        
        data['posts'].append(new_post)
        save_data(data)
        generate_site()
        return redirect(url_for('admin_dashboard', tab='blog', message='Post created!'))
    
    return render_template_string(ADMIN_EDIT_POST, post=None)

@app.route('/admin/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    data = load_data()
    post = next((p for p in data['posts'] if p['id'] == post_id), None)
    
    if not post:
        return redirect(url_for('admin_dashboard', tab='blog'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        word_count = len(content.split())
        read_time = f"{max(1, word_count // 200)} min"
        
        post['title'] = title
        post['slug'] = create_slug(title)
        post['excerpt'] = request.form.get('excerpt')
        post['content'] = content
        post['category'] = request.form.get('category')
        post['icon'] = request.form.get('icon')
        post['read_time'] = read_time
        post['published'] = 'published' in request.form
        
        save_data(data)
        generate_site()
        return redirect(url_for('admin_dashboard', tab='blog', message='Post updated!'))
    
    return render_template_string(ADMIN_EDIT_POST, post=post)

@app.route('/admin/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    data = load_data()
    post = next((p for p in data['posts'] if p['id'] == post_id), None)
    
    if post:
        html_file = os.path.join(OUTPUT_DIR, 'blog', f"{post['slug']}.html")
        if os.path.exists(html_file):
            os.remove(html_file)
        
        data['posts'] = [p for p in data['posts'] if p['id'] != post_id]
        save_data(data)
        generate_site()
    
    return redirect(url_for('admin_dashboard', tab='blog', message='Post deleted!'))

@app.route('/admin/regenerate')
@login_required
def regenerate():
    generate_site()
    return redirect(url_for('admin_dashboard', tab='blog', message='Site regenerated successfully!'))

if __name__ == '__main__':
    # Ensure footer exists in data
    data = load_data()
    if 'footer' not in data:
        data['footer'] = {
            'text': '© 2025 Mamdhooh Moomin Rasheed. Built for speed and security.',
            'tagline': 'root@mamdhooh:~$ whoami'
        }
        save_data(data)
    
    # Generate initial site
    generate_site()
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║  🚀 Complete Portfolio CMS - Running!                 ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Admin Panel: http://localhost:5000/admin             ║
    ║  Default Login: admin / admin123                      ║
    ║                                                       ║
    ║  Manage Everything:                                   ║
    ║  • Site Settings (name, email, social, footer)        ║
    ║  • Hero Section                                       ║
    ║  • Expertise Cards                                    ║
    ║  • Skills                                             ║
    ║  • Blog Posts                                         ║
    ║                                                       ║
    ║  Generated Files:                                     ║
    ║  • public/index.html (homepage + 1 featured post)     ║
    ║  • public/blog.html (all blog posts)                  ║
    ║  • public/blog/*.html (individual posts)              ║
    ║                                                       ║
    ║  Deploy 'public' folder to any static host!           ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, port=5000)