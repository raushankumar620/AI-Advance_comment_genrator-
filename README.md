# 🤖 AI Code Comment Generator & Analysis Platform

<div align="center">

![AI Code Assistant](https://img.shields.io/badge/AI-Code%20Assistant-blue?style=for-the-badge&logo=artificial-intelligence)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=for-the-badge&logo=javascript)

**A comprehensive AI-powered platform for intelligent code analysis, documentation, and security scanning**

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [API](#api-documentation) • [Contributing](#contributing)

</div>

---

## 🌟 Overview

Transform your code development workflow with our advanced AI-powered platform that provides intelligent code commenting, comprehensive security analysis, performance optimization suggestions, and automated documentation generation.

### 🎯 Key Highlights

- **🧠 Smart AI Commentary**: Advanced natural language processing for meaningful code comments
- **🛡️ Security Analysis**: Comprehensive vulnerability detection and prevention tips
- **⚡ Performance Insights**: Optimization suggestions and complexity analysis
- **📚 Auto Documentation**: Generate professional documentation automatically
- **🎨 Modern UI/UX**: Beautiful chatbot-style interface with smooth animations
- **🔧 Multi-Language Support**: Python, JavaScript, Java, C++, and more
- **📊 Quality Metrics**: Detailed code quality scoring and visualization

---

## ✨ Features

### 🤖 AI-Powered Analysis
- **Intelligent Code Comments**: Context-aware commenting using transformer models
- **Language Detection**: Automatic programming language identification
- **Code Structure Analysis**: Function, class, and import detection
- **Complexity Scoring**: Cyclomatic complexity calculation

### 🛡️ Security & Quality
- **Vulnerability Detection**: SQL injection, XSS, hardcoded credentials scanning
- **Code Quality Assessment**: Comprehensive quality scoring (0-100)
- **Performance Analysis**: Bottleneck detection and optimization tips
- **Best Practices**: Language-specific coding standard recommendations

### 🎨 User Experience
- **Chatbot Interface**: Conversational AI assistant experience
- **Real-time Analysis**: Instant feedback and results
- **Multiple Input Methods**: Paste code, upload files, or fetch from URLs
- **Export Options**: JSON, TXT, and HTML report generation
- **Responsive Design**: Works perfectly on desktop and mobile

### 🔧 Developer Tools
- **RESTful API**: Comprehensive API for integration
- **Batch Processing**: Analyze multiple code snippets simultaneously
- **Rate Limiting**: Built-in protection against abuse
- **Extensible Architecture**: Easy to add new analysis features

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/raushankumar620/code-comment-generator.git
   cd code-comment-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the platform**
   - Main Interface: http://localhost:5000
   - Advanced Analysis: http://localhost:5000/analyze
   - API Health: http://localhost:5000/api/health

---

## 📸 Demo

### Original Project Screenshot
![Project UI](https://github.com/raushankumar620/code-comment-generator/blob/main/Screenshot%202025-03-12%20154557.png)

### New Enhanced Features
- **Chatbot Interface**: Modern conversational UI
- **Advanced Analysis Dashboard**: Comprehensive code analysis
- **Security Scan Results**: Detailed vulnerability detection
- **Performance Insights**: Optimization recommendations

---

## 🛠️ Usage

### Basic Code Commenting

1. **Simple Comment Generation**
   ```python
   # Visit http://localhost:5000
   # Paste your code in the chat interface
   # Click send or press Ctrl+Enter
   # Get intelligent comments instantly
   ```

2. **Advanced Analysis**
   ```python
   # Visit http://localhost:5000/analyze
   # Choose analysis type (Full, Security, Performance, Comments)
   # Upload files or paste code
   # Get comprehensive analysis results
   ```

### API Usage

#### Generate Comments
```bash
curl -X POST http://localhost:5000/generate_comment \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello():\n    print(\"Hello World\")"}'
```

#### Comprehensive Analysis
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your_code_here",
    "analysis_type": "full"
  }'
```

---

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main chatbot interface |
| `GET` | `/analyze` | Advanced analysis dashboard |
| `POST` | `/generate_comment` | Basic comment generation |
| `POST` | `/api/analyze` | Comprehensive code analysis |
| `POST` | `/api/upload` | File upload and analysis |
| `POST` | `/api/batch-analyze` | Batch analysis (up to 10 files) |
| `POST` | `/api/export-report` | Export analysis results |
| `GET` | `/api/statistics` | Platform usage statistics |
| `GET` | `/api/health` | Health check endpoint |

### Analysis Types

- **`full`**: Complete analysis including comments, security, performance
- **`basic`**: Simple comment generation only
- **`security`**: Security vulnerability scanning
- **`performance`**: Performance optimization suggestions

---

## 🏗️ Architecture

### Project Structure
```
code-comment-generator/
├── 📁 static/                 # Static assets
│   ├── style.css             # Main stylesheet
│   ├── analyze.js            # Analysis page JavaScript
│   └── app.js                # Main app JavaScript
├── 📁 templates/             # HTML templates
│   ├── index.html            # Chatbot interface
│   └── analyze.html          # Analysis dashboard
├── 📄 app.py                 # Main Flask application
├── 📄 enhanced_comment_model.py # Advanced AI analysis engine
├── 📄 comment_model.py       # Basic comment generator
├── 📄 config.py              # Configuration management
├── 📄 utils.py               # Utility functions
├── 📄 requirements.txt       # Python dependencies
└── 📄 .env.example          # Environment variables template
```

### Tech Stack

#### Backend
- **Flask 2.3.3**: Web framework
- **Transformers 4.35.2**: AI/ML models
- **PyTorch 2.1.0**: Deep learning framework
- **OpenAI API**: Advanced language models
- **AST**: Python code analysis
- **Pygments**: Syntax highlighting

#### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript ES6+**: Interactive functionality
- **Chart.js**: Data visualization
- **Prism.js**: Code syntax highlighting
- **Font Awesome**: Icons

---

## 🧪 Original vs Enhanced Comparison

### Original Features
✔️ **AI-based Comment Generation** using `T5 Transformer`  
✔️ **Manual Commenting for Simple Code Blocks**  
✔️ **Interactive Web Interface** built with Flask & JavaScript  
✔️ **Supports Multi-line Code Input**  
✔️ **Fast & Accurate Commenting**  

### New Enhanced Features
🚀 **Advanced Security Scanning** - SQL injection, XSS, credential detection  
🚀 **Performance Analysis** - Complexity scoring, optimization tips  
🚀 **Multi-Language Support** - Python, JavaScript, Java, C++, etc.  
🚀 **Chatbot Interface** - Modern conversational UI experience  
🚀 **Comprehensive Dashboard** - Advanced analysis with visualizations  
🚀 **Export Capabilities** - JSON, TXT reports with sharing options  
🚀 **File Upload Support** - Analyze entire files, not just snippets  
🚀 **Batch Processing** - Multiple file analysis simultaneously  
🚀 **Rate Limiting** - Production-ready with abuse protection  
🚀 **Quality Metrics** - Code quality scoring and recommendations  

---

## ⚙️ Configuration

### Environment Variables

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# AI Models
OPENAI_API_KEY=your-openai-api-key  # Optional
DEFAULT_MODEL=t5-base

# Features
ENABLE_CODE_ANALYSIS=True
ENABLE_SECURITY_SCAN=True
ENABLE_PERFORMANCE_ANALYSIS=True

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=30

# Deployment
PORT=5000
```

---

## 🤝Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Original Creator**: [Raushan Kumar](https://github.com/raushankumar620) for the initial concept
- **Hugging Face Transformers**: For providing excellent AI models
- **OpenAI**: For advanced language model capabilities
- **Flask Community**: For the robust web framework

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Enhanced with ❤️ by the AI Code Assistant Team

</div>
cd code-comment-generator
