# Portfolio CMS - Static Site Generator

A blazing-fast, lightweight portfolio and blog CMS that generates pure HTML files. Perfect for security professionals, developers, and anyone who wants a lightning-fast static website.

## 🚀 Features

- ✅ **Complete CMS** - Manage everything through a web interface
- ✅ **Pure HTML Output** - No JavaScript frameworks, just fast-loading pages
- ✅ **Blog System** - Full markdown support for writing posts
- ✅ **Ultra Lightweight** - ~10KB pages that load instantly
- ✅ **SEO Optimized** - Static HTML with proper meta tags
- ✅ **Deploy Anywhere** - Upload to any static host (Netlify, Vercel, GitHub Pages, etc.)
- ✅ **Auto-Regeneration** - Site rebuilds on every save
- ✅ **Modern Design** - Dark theme with neon green accents

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/medoish/portfolio-cms.git
cd portfolio-cms
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:

```bash
# Flask Configuration
SECRET_KEY=your-random-secret-key-here

# Environment
FLASK_ENV=production
FLASK_DEBUG=False

# Admin Credentials - CHANGE THESE!
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# Server Configuration
PORT=5000
HOST=127.0.0.1
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the application
```bash
python app.py
```

### 6. Access the admin panel
- Open `http://localhost:5000/admin`
- Login with credentials from `.env`
- Start customizing your site!

## 🎨 What You Can Manage

### Site Settings Tab
- **Site Info**: Name, title, description, email, Twitter handle
- **Hero Section**: Tag line, main title, description
- **Footer**: Terminal tagline and footer text

### Content Tab
- **Expertise Cards**: Add/edit/delete expertise sections with icons
- **Skills**: Comma-separated list of skills and technologies

### Blog Tab
- **Create Posts**: Write in markdown with live preview
- **Edit Posts**: Update existing blog posts
- **Publish/Unpublish**: Control post visibility
- **Categories**: Security, Development, Red Team, Tools, Research, DevSecOps
- **Auto-generation**: HTML files created automatically

## 📁 Project Structure

```
portfolio-cms/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── site_data.json        # All your content (auto-generated)
└── public/               # Generated static files
    ├── index.html        # Homepage with 1 featured post
    ├── blog.html         # Blog listing page (all posts)
    └── blog/             # Individual blog posts
        ├── post-1.html
        └── post-2.html
```

## 🚀 Deployment

Your static files are generated in the `public/` folder. Deploy this folder to any static hosting service:

### Option 1: Netlify (Easiest)
1. Go to [Netlify](https://www.netlify.com/)
2. Drag and drop the `public/` folder
3. Done! Your site is live

### Option 2: Vercel
```bash
npm install -g vercel
vercel --prod public/
```

### Option 3: GitHub Pages
1. Push `public/` to a GitHub repo
2. Enable GitHub Pages in Settings
3. Select the folder with your HTML

### Option 4: Traditional Hosting
Upload the `public/` folder via FTP to any web host.

## 📝 Writing Blog Posts

The CMS supports markdown:

```markdown
# Main Header
## Sub Header

**Bold text** and _italic text_

- Bullet point 1
- Bullet point 2

1. Numbered list
2. Second item

`inline code`

```
code block
```

> Blockquote
```

## 🎯 Customization

### Change Colors
Edit `BASE_CSS` in `app.py`:
```python
:root{
    --bg:#0a0a0a;           # Background
    --card:#1a1a1a;         # Card background
    --text:#fff;            # Text color
    --accent:#00ff88;       # Accent (green)
    --border:#2a2a2a        # Borders
}
```

### Add New Sections
Modify HTML generation functions:
- `generate_index_html()` - Homepage
- `generate_blog_page_html()` - Blog listing
- `generate_post_html()` - Individual posts

### Custom Domain
1. Deploy `public/` folder to host
2. Configure DNS to point to hosting provider
3. Add custom domain in hosting settings

## 🔐 Security Notes

- ✅ Change default credentials in `.env`
- ✅ Use strong SECRET_KEY in production
- ✅ Never commit `.env` to version control
- ✅ Enable HTTPS in production
- ✅ Set `FLASK_DEBUG=False` in production

## 🐛 Troubleshooting

**Site not regenerating?**
- Click "Regenerate Site" in admin panel
- Check file permissions on `public/` folder

**Can't login?**
- Verify `.env` file exists and has correct credentials
- Check that `python-dotenv` is installed

**Port already in use?**
- Change `PORT` in `.env` file
- Or stop other Flask applications

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

## 📊 Performance

- **Page Size**: ~10KB (homepage)
- **Load Time**: <100ms (on good hosting)
- **Lighthouse Score**: 100/100
- **No JavaScript**: Pure HTML for maximum speed

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Pure HTML + CSS (no frameworks)
- **Storage**: JSON file
- **Deployment**: Static files (any host)

## 📄 License

MIT License - Free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! 

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 👤 Author

**Mamdhooh Moomin Rasheed**
- Website: [mamdhooh.com](https://mamdhooh.com)
- Twitter: [@moominrasheed](https://x.com/moominrasheed)
- Email: letstalk@mamdhooh.com

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Built for speed. Built for security. Built with Python.** 🐍⚡


================== .gitignore ==================
# Environment Variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Site Data (optional - uncomment if you don't want to commit your content)
# site_data.json

# Generated Static Files (optional - uncomment if you don't want to commit generated files)
# public/

# Logs
*.log
logs/

# OS
Thumbs.db
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/


================== .env (EXAMPLE - CREATE YOUR OWN) ==================
# Flask Configuration
# Generate a random secret key: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=change-this-to-a-random-secret-key-in-production

# Environment
FLASK_ENV=production
FLASK_DEBUG=False

# Admin Credentials - CHANGE THESE!
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Server Configuration
PORT=5000
HOST=127.0.0.1