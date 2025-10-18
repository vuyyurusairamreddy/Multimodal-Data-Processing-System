# Multimodal Data Processing System

A comprehensive RAG (Retrieval Augmented Generation) system that processes multimodal input files and responds to natural language queries using Perplexity Sonar Pro API.

## Features

- Process multiple file types: PDF, DOCX, PPTX, TXT, MD
- Image text extraction: PNG, JPG, JPEG
- Audio/Video transcription: MP3, MP4, WAV, M4A, AVI, MOV, MKV
- YouTube video download and transcription
- Natural language query interface powered by Perplexity Sonar Pro
- Semantic search with sentence embeddings
- SQLite database for knowledge base storage
- User-friendly Streamlit interface

## System Requirements

- Python 3.8 or higher
- FFmpeg (for audio/video processing)
- Tesseract OCR (for image text extraction)
- 4GB RAM minimum
- 2GB free disk space

## Installation Guide

### Step 1: Clone or Download Project

Create a project folder and set up the file structure as provided.

### Step 2: Install Python Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Install System Dependencies

#### Installing FFmpeg

**Windows:**
1. Download FFmpeg from https://www.ffmpeg.org/download.html
2. Click on Windows icon and select "Windows builds from gyan.dev"
3. Download the `ffmpeg-git-full.7z` file
4. Extract using 7-Zip to your Downloads folder
5. Rename folder to `ffmpeg` and move to `C:\` drive
6. Add to System PATH:
   - Press Windows Key + S and search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", find and select "Path"
   - Click "Edit" and add new entry: `C:\ffmpeg\bin`
   - Click OK on all windows
7. Restart Command Prompt and verify:
```bash
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Installing Tesseract OCR

**Windows:**
1. Download from https://github.com/UB-Mannheim/tesseract/wiki
2. Download `tesseract-ocr-w64-setup-5.x.x.exe`
3. Run the installer
4. Install to default location: `C:\Program Files\Tesseract-OCR`
5. Add to System PATH:
   - Press Windows Key + S and search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", select "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\Tesseract-OCR`
   - Click OK on all windows
6. Restart Command Prompt and verify:
```bash
tesseract --version
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

### Step 4: Get Perplexity API Key

1. Visit https://www.perplexity.ai/
2. Create an account or log in
3. Navigate to https://www.perplexity.ai/settings/api
4. Click on "API" tab
5. Click "Generate API Key" button
6. Copy the generated key (starts with "pplx-")
7. Store it securely - it will only be shown once

**Note:** API pricing ranges from $0.2 to $5 per million tokens for Sonar models. Pro subscribers receive $5 monthly API credit.

### Step 5: Configure API Key

Open `config.py` and replace the placeholder with your actual API key:

```python
PERPLEXITY_API_KEY = "pplx-your-actual-api-key-here"
```

**Important:** Never commit your API key to version control or share it publicly.

## How to Execute

### Running the Application

1. Open terminal/command prompt in the project directory

2. Activate virtual environment (recommended):

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

4. The application will automatically open in your default browser at `http://localhost:8501`

5. If it doesn't open automatically, manually navigate to the URL shown in terminal

### Using the Application

#### Tab 1: Upload Files

**Option A: File Upload**
1. Click "Browse files" button
2. Select one or multiple files (PDF, DOCX, PPTX, TXT, MD, PNG, JPG, MP3, MP4, etc.)
3. Click "Process Uploaded Files" button
4. Wait for processing to complete
5. Success messages will appear for each processed file

**Option B: YouTube URL**
1. Select "YouTube URL" radio button
2. Enter YouTube video URL
3. Click "Process YouTube Video" button
4. Wait for download and transcription to complete

#### Tab 2: Ask Questions

1. Type your question in the text area
2. Click "Get Answer" button
3. View the AI-generated answer based on your knowledge base
4. See relevant documents used to generate the answer
5. Check recent query history at the bottom

#### Tab 3: View Knowledge Base

1. View total number of processed documents
2. Expand each document to see:
   - File type
   - Content preview
   - Metadata

## Project Structure

```
multimodal_rag_system/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration and API keys
├── README.md                   # This file
│
├── data/
│   ├── uploads/                # Uploaded files (auto-created)
│   └── knowledge_base.db       # SQLite database (auto-created)
│
├── processors/
│   ├── __init__.py
│   ├── text_processor.py       # PDF, DOCX, PPTX, TXT, MD processing
│   ├── image_processor.py      # Image OCR processing
│   ├── audio_processor.py      # Audio/video transcription
│   └── youtube_processor.py    # YouTube video processing
│
└── utils/
    ├── __init__.py
    ├── database.py             # SQLite operations
    ├── embeddings.py           # Embedding generation
    └── query_handler.py        # Perplexity API integration
```

## Troubleshooting

### FFmpeg not found
- Verify FFmpeg is installed: `ffmpeg -version`
- Check PATH environment variable includes FFmpeg bin directory
- Restart terminal/command prompt after PATH changes
- Restart computer if changes don't take effect

### Tesseract not found
- Verify Tesseract is installed: `tesseract --version`
- Check PATH environment variable includes Tesseract directory
- On Windows, may need to specify path in code:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
- Add this line at the top of `processors/image_processor.py` if needed

### API Key Error
- Verify API key is correctly set in `config.py`
- Check for extra spaces or quotes
- Ensure you have active credits in Perplexity account
- Visit https://www.perplexity.ai/settings/api to check API status
- API usage is pay-as-you-go ($0.2-$5 per million tokens)

### Module Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using correct Python version (3.8+)
- Try upgrading pip: `pip install --upgrade pip`
- Check if virtual environment is activated

### Database Permission Errors
- Ensure `data/` directory exists
- Check write permissions for project directory
- Delete `knowledge_base.db` and restart to recreate

### Streamlit Not Opening
- Manually open browser and go to `http://localhost:8501`
- Check if port 8501 is already in use
- Try different port: `streamlit run app.py --server.port 8502`

### Whisper Model Download Issues
- First run will download Whisper model (approx 140MB)
- Ensure stable internet connection
- If download fails, manually download from: https://github.com/openai/whisper
- Place model in cache directory

## Usage Tips

1. **Supported File Types:**
   - Documents: PDF, DOCX, PPTX, TXT, MD
   - Images: PNG, JPG, JPEG
   - Audio: MP3, WAV, M4A
   - Video: MP4, AVI, MOV, MKV
   - YouTube: Any valid YouTube URL

2. **Best Practices:**
   - Process documents before asking questions
   - Use clear, specific questions for better answers
   - Upload related documents together for coherent knowledge base
   - Review relevant documents to understand answer sources

3. **Performance:**
   - Large video files may take several minutes to process
   - First query may be slower due to embedding model loading
   - Consider processing files in batches if uploading many documents
   - YouTube videos download audio only (more efficient)

4. **API Usage:**
   - Monitor your API usage to control costs
   - Pro subscribers get $5 monthly credit
   - Usage is token-based ($0.2-$5 per million tokens)
   - Complex queries with citations use more tokens

## Technical Details

- **LLM:** Perplexity Sonar Pro API
- **Embedding Model:** all-MiniLM-L6-v2 (sentence-transformers)
- **Database:** SQLite with BLOB storage for embeddings
- **Transcription:** OpenAI Whisper (base model)
- **OCR:** Tesseract 4.0+
- **UI Framework:** Streamlit 1.39.0
- **YouTube Downloader:** yt-dlp

## Security Notes

- Keep your Perplexity API key confidential
- Do not commit `config.py` with real API keys to version control
- Consider using environment variables for production:
```python
import os
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
```
- Add `config.py` to `.gitignore` file
- Never share API keys publicly

## Known Limitations

- Maximum file size depends on available RAM
- Whisper base model supports English best (multilingual available)
- OCR accuracy depends on image quality
- API rate limits apply based on Perplexity subscription
- Large videos require significant processing time

## Future Enhancements

- Support for more file formats (EPUB, CSV, JSON)
- Multi-language support for transcription
- Advanced search filters
- Export knowledge base feature
- Batch processing queue
- Custom embedding models
- Vector database integration (FAISS, Pinecone)

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all system dependencies are installed
3. Review terminal/command prompt for error messages
4. Check Perplexity API documentation: https://docs.perplexity.ai/

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## License

This project is provided as-is for educational and development purposes.

## Acknowledgments

- Perplexity AI for Sonar Pro API
- OpenAI for Whisper transcription model
- Sentence Transformers for embedding models
- Streamlit for the UI framework
- All open-source libraries used in this project

## Version History

- **v1.0.0** (October 2025) - Initial release
  - Multimodal file processing
  - Perplexity Sonar Pro integration
  - SQLite knowledge base
  - Streamlit interface

---