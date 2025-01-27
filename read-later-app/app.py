from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    links = db.relationship('Link', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    favorite = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'favorite': self.favorite
        }

def get_link_preview(url):
    preview_data = {
        'title': url,
        'description': 'No description available',
        'image': ''
    }
    
    print(f"\nFetching preview for URL: {url}")
    
    # Try microlink.io API first (it's free and reliable)
    try:
        print("Making request to microlink API...")
        api_url = "https://api.microlink.io"
        params = {'url': url}
        
        response = requests.get(api_url, params=params, timeout=10)
        print(f"Microlink API response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            try:
                api_data = response.json()
                print(f"Microlink API data: {api_data}")
                data = api_data.get('data', {})
                
                if data.get('image', {}).get('url'):
                    preview_data['image'] = data['image']['url']
                if data.get('title'):
                    preview_data['title'] = data['title']
                if data.get('description'):
                    preview_data['description'] = data['description'][:200] + '...'
                
                if preview_data['image']:  # If we got an image, return immediately
                    print("Successfully fetched preview from Microlink API")
                    return preview_data
            except Exception as e:
                print(f"Error parsing Microlink API response: {e}")
    except Exception as e:
        print(f"Error fetching from Microlink API: {e}")
    
    # If API fails, try scraping with extended image search
    try:
        print("\nFalling back to web scraping...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"Scraping response status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to get title
            if soup.title:
                preview_data['title'] = soup.title.string.strip()
                print(f"Found title: {preview_data['title']}")
            
            # Try to get description
            for desc_tag in ['description', 'og:description', 'twitter:description']:
                meta_desc = soup.find('meta', attrs={'name': desc_tag}) or soup.find('meta', attrs={'property': desc_tag})
                if meta_desc and meta_desc.get('content'):
                    preview_data['description'] = meta_desc['content'].strip()[:200] + '...'
                    print(f"Found description from {desc_tag}")
                    break
            
            # Try to get image - check all possible sources
            if not preview_data['image']:
                # Check meta tags first
                meta_img_tags = [
                    ('meta', 'og:image'),
                    ('meta', 'twitter:image'),
                    ('meta', 'thumbnail'),
                    ('link', 'image_src'),
                    ('link', 'apple-touch-icon'),
                ]
                
                for tag_type, tag_name in meta_img_tags:
                    img_tag = (soup.find(tag_type, attrs={'property': tag_name}) or 
                             soup.find(tag_type, attrs={'name': tag_name}) or 
                             soup.find(tag_type, attrs={'rel': tag_name}))
                    
                    if img_tag:
                        img_url = img_tag.get('content') or img_tag.get('href')
                        if img_url:
                            if not img_url.startswith(('http://', 'https://', 'data:')):
                                img_url = urljoin(url, img_url)
                            preview_data['image'] = img_url
                            print(f"Found image from {tag_name}: {img_url}")
                            break
                
                # If still no image, look for the largest image in content
                if not preview_data['image']:
                    print("Looking for images in content...")
                    imgs = soup.find_all('img')
                    max_size = 0
                    best_img = None
                    
                    for img in imgs:
                        src = img.get('src', '')
                        if src and not src.startswith('data:'):
                            # Check for common image attributes that might indicate a featured image
                            width = img.get('width', '0')
                            height = img.get('height', '0')
                            try:
                                size = int(width) * int(height) if width and height else 0
                            except ValueError:
                                size = 0
                            
                            # Also consider if image is in an article tag or has certain classes
                            in_article = bool(img.find_parent('article'))
                            has_feature_class = any(c for c in img.get('class', []) if 'feature' in c.lower() or 'hero' in c.lower())
                            
                            if size > max_size or in_article or has_feature_class:
                                max_size = size
                                best_img = src
                    
                    if best_img:
                        if not best_img.startswith(('http://', 'https://')):
                            best_img = urljoin(url, best_img)
                        preview_data['image'] = best_img
                        print(f"Found best content image: {best_img}")
    
    except Exception as e:
        print(f"Error during web scraping: {e}")
        traceback.print_exc()
    
    print(f"Final preview data: {preview_data}")
    return preview_data

@app.route('/')
def index():
    category_id = request.args.get('category', type=int)
    uncategorized = request.args.get('uncategorized', type=int)
    favorites_only = request.args.get('favorites', type=int)
    search_query = request.args.get('q', '').strip()
    
    # If no filters are applied, redirect to uncategorized by default
    if not any([category_id, uncategorized, favorites_only, search_query]):
        return redirect('/?uncategorized=1')
    
    # Start with base query
    query = Link.query
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    elif uncategorized:
        query = query.filter_by(category_id=None)
    
    # Apply search if provided
    if search_query:
        search_filter = (Link.title.ilike(f'%{search_query}%') |
                        Link.description.ilike(f'%{search_query}%') |
                        Link.url.ilike(f'%{search_query}%'))
        query = query.filter(search_filter)
    
    # Apply favorites filter
    if favorites_only:
        query = query.filter_by(favorite=True)
    
    # Get final results
    links = query.order_by(Link.created_at.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('index.html', 
                         links=links, 
                         categories=categories, 
                         current_category=category_id,
                         uncategorized=uncategorized,
                         search_query=search_query,
                         favorites_only=favorites_only)

@app.route('/add', methods=['POST'])
def add_link():
    url = request.form.get('link')
    category_id = request.form.get('category_id', type=int)
    
    if url:
        preview_data = get_link_preview(url)
        new_link = Link(
            url=url,
            title=preview_data['title'],
            description=preview_data['description'],
            image=preview_data['image'],
            category_id=category_id
        )
        db.session.add(new_link)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_link(id):
    link = Link.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    
    # Preserve URL parameters when redirecting
    params = []
    if request.args.get('q'):
        params.append(f"q={request.args.get('q')}")
    if request.args.get('favorites'):
        params.append("favorites=1")
    if request.args.get('category'):
        params.append(f"category={request.args.get('category')}")
    if request.args.get('uncategorized'):
        params.append("uncategorized=1")
    
    redirect_url = '/?' + '&'.join(params) if params else '/'
    return redirect(redirect_url)

@app.route('/category', methods=['POST'])
def add_category():
    name = request.form.get('name')
    if name:
        category = Category(name=name)
        try:
            db.session.add(category)
            db.session.commit()
        except:
            db.session.rollback()
    return redirect('/')

@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False}), 500

@app.route('/update_category/<int:link_id>', methods=['POST'])
def update_category(link_id):
    data = request.get_json()
    link = Link.query.get_or_404(link_id)
    category_id = data.get('category_id')
    
    if category_id:
        category = Category.query.get_or_404(category_id)
        link.category = category
    else:
        link.category = None
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/toggle_favorite/<int:id>', methods=['POST'])
def toggle_favorite(id):
    link = Link.query.get_or_404(id)
    link.favorite = not link.favorite
    db.session.commit()
    return jsonify({'success': True, 'favorite': link.favorite})

if __name__ == '__main__':
    with app.app_context():
        # Create tables only if they don't exist
        db.create_all()
    app.run(debug=True)
