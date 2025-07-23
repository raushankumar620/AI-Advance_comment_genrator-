
"""
Enhanced Code Analysis and Documentation Platform
Advanced Flask application with comprehensive code analysis features
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import time
from datetime import datetime
import logging
from functools import wraps
from collections import defaultdict
import io
import zipfile

from config import Config
from enhanced_comment_model import analyze_code, generate_comment
from comment_model import generate_comment as basic_generate_comment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Rate limiting storage (in production, use Redis)
rate_limit_storage = defaultdict(list)

def rate_limit(max_requests=30):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old requests
            rate_limit_storage[client_ip] = [
                req_time for req_time in rate_limit_storage[client_ip]
                if current_time - req_time < 60  # 1 minute window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_requests:
                return jsonify({
                    "error": "Rate limit exceeded. Please try again later.",
                    "retry_after": 60
                }), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    """Serve the advanced analysis page"""
    return render_template('analyze.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

@app.route('/generate_comment', methods=['POST'])
@rate_limit(max_requests=app.config['MAX_REQUESTS_PER_MINUTE'])
def generate_comment_api():
    """Basic comment generation API (backward compatibility)"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({"error": "No code provided!"}), 400

        if len(code) > 50000:  # 50KB limit
            return jsonify({"error": "Code too large. Maximum 50KB allowed."}), 413

        # Use basic model for simple requests
        commented_code = basic_generate_comment(code)
        
        return jsonify({
            "commented_code": commented_code,
            "processing_time": time.time() - request.start_time if hasattr(request, 'start_time') else 0
        })

    except Exception as e:
        logger.error(f"Error in generate_comment_api: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/analyze', methods=['POST'])
@rate_limit(max_requests=20)  # Lower limit for intensive analysis
def comprehensive_analysis_api():
    """Advanced code analysis API"""
    try:
        start_time = time.time()
        data = request.get_json()
        code = data.get('code', '').strip()
        analysis_type = data.get('analysis_type', 'full')  # basic, full, security, performance

        if not code:
            return jsonify({"error": "No code provided!"}), 400

        if len(code) > 100000:  # 100KB limit for analysis
            return jsonify({"error": "Code too large for analysis. Maximum 100KB allowed."}), 413

        # Perform comprehensive analysis
        result = analyze_code(code)
        
        # Filter results based on analysis type
        if analysis_type == 'basic':
            filtered_result = {
                'commented_code': result['commented_code'],
                'language': result['language'],
                'lines_of_code': result['lines_of_code']
            }
        elif analysis_type == 'security':
            filtered_result = {
                'security_issues': result['security_issues'],
                'language': result['language']
            }
        elif analysis_type == 'performance':
            filtered_result = {
                'performance_suggestions': result['performance_suggestions'],
                'complexity_score': result['complexity_score'],
                'language': result['language']
            }
        else:  # full analysis
            filtered_result = result

        # Add metadata
        filtered_result.update({
            'processing_time': time.time() - start_time,
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        })

        return jsonify(filtered_result)

    except Exception as e:
        logger.error(f"Error in comprehensive_analysis_api: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST'])
@rate_limit(max_requests=10)  # Lower limit for file uploads
def upload_file():
    """Handle file uploads for analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": f"File type not supported. Allowed types: {', '.join(app.config['ALLOWED_EXTENSIONS'])}"
            }), 400

        # Read file content
        content = file.read().decode('utf-8', errors='ignore')
        
        if len(content) > 200000:  # 200KB limit for uploaded files
            return jsonify({"error": "File too large. Maximum 200KB allowed."}), 413

        # Analyze the uploaded code
        result = analyze_code(content)
        result.update({
            'filename': secure_filename(file.filename),
            'file_size': len(content),
            'upload_timestamp': datetime.now().isoformat()
        })

        return jsonify(result)

    except UnicodeDecodeError:
        return jsonify({"error": "File encoding not supported. Please use UTF-8."}), 400
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        return jsonify({"error": f"File processing failed: {str(e)}"}), 500

@app.route('/api/batch-analyze', methods=['POST'])
@rate_limit(max_requests=5)  # Very low limit for batch processing
def batch_analyze():
    """Analyze multiple code snippets"""
    try:
        data = request.get_json()
        code_snippets = data.get('code_snippets', [])
        
        if not code_snippets or len(code_snippets) > 10:
            return jsonify({"error": "Provide 1-10 code snippets"}), 400

        results = []
        total_start_time = time.time()

        for i, snippet in enumerate(code_snippets):
            if len(snippet) > 10000:  # 10KB limit per snippet
                results.append({
                    'index': i,
                    'error': 'Code snippet too large'
                })
                continue

            try:
                result = analyze_code(snippet)
                result['index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e)
                })

        return jsonify({
            'results': results,
            'total_processing_time': time.time() - total_start_time,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in batch_analyze: {e}")
        return jsonify({"error": f"Batch analysis failed: {str(e)}"}), 500

@app.route('/api/export-report', methods=['POST'])
@rate_limit(max_requests=5)
def export_report():
    """Export analysis report"""
    try:
        data = request.get_json()
        analysis_result = data.get('analysis_result', {})
        export_format = data.get('format', 'json')  # json, txt, html

        if not analysis_result:
            return jsonify({"error": "No analysis result provided"}), 400

        if export_format == 'json':
            # Create JSON report
            report = json.dumps(analysis_result, indent=2)
            
            # Create in-memory file
            output = io.StringIO()
            output.write(report)
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='application/json',
                as_attachment=True,
                download_name=f'code_analysis_report_{int(time.time())}.json'
            )

        elif export_format == 'txt':
            # Create text report
            report_lines = [
                "CODE ANALYSIS REPORT",
                "=" * 50,
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Language: {analysis_result.get('language', 'Unknown')}",
                f"Lines of Code: {analysis_result.get('lines_of_code', 'N/A')}",
                f"Quality Score: {analysis_result.get('code_quality_score', 'N/A')}",
                "",
                "SECURITY ISSUES:",
                "-" * 20
            ]
            
            for issue in analysis_result.get('security_issues', []):
                report_lines.append(f"- {issue.get('type', 'Unknown')}: Line {issue.get('line', 'N/A')}")
            
            report_lines.extend([
                "",
                "PERFORMANCE SUGGESTIONS:",
                "-" * 30
            ])
            
            for suggestion in analysis_result.get('performance_suggestions', []):
                report_lines.append(f"- {suggestion}")
            
            report = '\n'.join(report_lines)
            
            return send_file(
                io.BytesIO(report.encode()),
                mimetype='text/plain',
                as_attachment=True,
                download_name=f'code_analysis_report_{int(time.time())}.txt'
            )

        else:
            return jsonify({"error": "Unsupported export format"}), 400

    except Exception as e:
        logger.error(f"Error in export_report: {e}")
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get platform statistics"""
    try:
        # In production, these would come from a database
        stats = {
            'total_analyses': 1234,
            'languages_supported': len(app.config['ALLOWED_EXTENSIONS']),
            'average_processing_time': 2.3,
            'security_issues_found': 89,
            'uptime': '99.9%',
            'version': '2.0.0',
            'features_enabled': {
                'code_analysis': app.config['ENABLE_CODE_ANALYSIS'],
                'security_scan': app.config['ENABLE_SECURITY_SCAN'],
                'performance_analysis': app.config['ENABLE_PERFORMANCE_ANALYSIS']
            }
        }
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in get_statistics: {e}")
        return jsonify({"error": "Failed to get statistics"}), 500

@app.before_request
def before_request():
    """Log requests and add timing"""
    request.start_time = time.time()
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Log response timing"""
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        logger.info(f"Request completed in {duration:.3f}s with status {response.status_code}")
    
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors"""
    return jsonify({"error": "File or request too large"}), 413

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Run the Flask app
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
