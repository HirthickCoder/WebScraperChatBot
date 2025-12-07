# Web Scraping Chatbot 🤖

A modern web scraping chatbot with a stylish dark green UI that allows you to scrape any website and chat with its content using AI-powered responses.

## Features ✨

- 🌐 **Web Scraping**: Extract content from any URL using BeautifulSoup
- 💬 **Intelligent Chat**: Ask questions about scraped content
- 🎨 **Dark Green Theme**: Beautiful, modern UI with smooth animations
- ⚡ **Real-time Processing**: Instant scraping and chat responses
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🔒 **Secure**: Input validation and XSS protection

## Tech Stack 🛠️

### Backend
- **Flask**: Python web framework
- **BeautifulSoup4**: Web scraping library
- **Requests**: HTTP library
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Vanilla JS for interactivity
- **Inter Font**: Professional typography

## Installation 📦

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd c:\Users\Hirthick\Downloads\website-to-chatbot-main
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file (optional)**
```bash
copy .env.example .env
```

## Usage 🚀

### Starting the Backend

1. **Run the Flask server**
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Using the Frontend

1. **Open the HTML file**
   - Simply open `index.html` in your web browser
   - Or use a local server:
   ```bash
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

2. **Scrape a Website**
   - Enter a URL in the scraper section (e.g., `https://example.com`)
   - Click the "Scrape" button
   - Wait for the content to be extracted

3. **Chat with the Content**
   - Once scraped, ask questions in the chat section
   - Examples:
     - "What is this page about?"
     - "What is the title?"
     - "Show me the links"
     - "Summarize the content"

## API Documentation 📚

### Endpoints

#### Health Check
```
GET /health
```
Returns the API health status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Web Scraping Chatbot API is running"
}
```

#### Scrape Website
```
POST /scrape
```
Scrapes content from a provided URL.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "Extracted content...",
  "links": [
    {"text": "Link text", "url": "https://..."}
  ],
  "content_length": 1234
}
```

#### Chat
```
POST /chat
```
Process user questions about scraped content.

**Request Body:**
```json
{
  "message": "What is this page about?",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Based on the content from Example Domain...",
  "source": "https://example.com"
}
```

#### Clear Data
```
POST /clear
```
Clear scraped data from memory.

**Request Body:**
```json
{
  "url": "https://example.com"  // Optional, clears all if omitted
}
```

## Project Structure 📁

```
website-to-chatbot-main/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── index.html            # Main HTML interface
├── style.css             # Dark green theme styles
├── script.js             # Frontend JavaScript
├── .env.example          # Environment variables template
└── README_CHATBOT.md     # This file
```

## Customization 🎨

### Changing Colors

Edit the CSS variables in `style.css`:

```css
:root {
    --primary-dark: #0a3d2e;      /* Dark green */
    --primary-medium: #1a5c47;    /* Medium green */
    --primary-light: #2d8659;     /* Light green */
    --accent-green: #3dbd7d;      /* Accent green */
    --accent-bright: #4dd694;     /* Bright accent */
}
```

### Modifying Scraping Behavior

Edit the `scrape_website()` function in `app.py` to:
- Change content extraction logic
- Add more metadata
- Filter specific content types
- Customize cleaning rules

## Deployment 🌍

### Option 1: Render (Backend)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variable: `PORT=10000`

### Option 2: Netlify (Frontend)

1. Deploy `index.html`, `style.css`, and `script.js`
2. Update `API_BASE_URL` in `script.js` to your backend URL

### Option 3: Heroku

1. Create `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Troubleshooting 🔧

### Backend not connecting
- Ensure Flask server is running on port 5000
- Check CORS settings in `app.py`
- Verify firewall settings

### Scraping fails
- Some websites block scrapers (use headers)
- Check URL format (must include http:// or https://)
- Verify internet connection

### Chat not working
- Scrape a website first before chatting
- Check browser console for errors
- Ensure backend is responding

## Limitations ⚠️

- Scraped data is stored in memory (cleared on server restart)
- Some websites may block scraping attempts
- JavaScript-heavy sites may not scrape completely
- Rate limiting not implemented (add for production)

## Future Enhancements 🚀

- [ ] Add database for persistent storage
- [ ] Implement AI/LLM integration for better responses
- [ ] Add user authentication
- [ ] Support for multiple concurrent scraping sessions
- [ ] Export scraped data (JSON, CSV)
- [ ] Advanced filtering and search
- [ ] Scheduled scraping
- [ ] Webhook notifications

## License 📄

MIT License - Feel free to use and modify!

## Support 💬

For issues or questions, please check:
- Backend logs in terminal
- Browser console for frontend errors
- Network tab for API calls

## Credits 👏

Built with ❤️ using Flask, BeautifulSoup, and modern web technologies.

---

**Happy Scraping! 🎉**
