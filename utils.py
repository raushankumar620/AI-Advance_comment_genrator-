"""
Utility functions for the code analysis platform
"""

import re
import hashlib
import time
from typing import List, Dict, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def validate_code_input(code: str, max_length: int = 100000) -> Dict[str, Any]:
    """Validate code input"""
    if not code or not code.strip():
        return {"valid": False, "error": "Code cannot be empty"}
    
    if len(code) > max_length:
        return {"valid": False, "error": f"Code too large. Maximum {max_length} characters allowed"}
    
    # Check for potentially malicious content
    dangerous_patterns = [
        r'__import__\s*\(\s*[\'"]os[\'"]',
        r'exec\s*\(',
        r'eval\s*\(',
        r'subprocess\.',
        r'os\.system',
        r'open\s*\(\s*[\'"][^\'\"]*[\'"],\s*[\'"]w',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return {"valid": False, "error": "Code contains potentially dangerous operations"}
    
    return {"valid": True}

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:90] + ('.' + ext if ext else '')
    return filename

def generate_analysis_id(code: str) -> str:
    """Generate unique ID for analysis"""
    return hashlib.md5(f"{code}{time.time()}".encode()).hexdigest()[:16]

def format_processing_time(seconds: float) -> str:
    """Format processing time for display"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s"

def extract_code_metrics(code: str) -> Dict[str, int]:
    """Extract basic code metrics"""
    lines = code.split('\n')
    
    metrics = {
        'total_lines': len(lines),
        'non_empty_lines': len([line for line in lines if line.strip()]),
        'comment_lines': len([line for line in lines if line.strip().startswith(('#', '//', '/*'))]),
        'avg_line_length': sum(len(line) for line in lines) // max(len(lines), 1),
        'max_line_length': max(len(line) for line in lines) if lines else 0,
    }
    
    metrics['comment_ratio'] = metrics['comment_lines'] / max(metrics['non_empty_lines'], 1) * 100
    
    return metrics

def detect_language_heuristics(code: str) -> str:
    """Detect programming language using simple heuristics"""
    code_lower = code.lower()
    
    # Python indicators
    if any(keyword in code for keyword in ['def ', 'import ', 'from ', 'elif ', 'pass']):
        return 'python'
    
    # JavaScript indicators
    if any(keyword in code for keyword in ['function ', 'const ', 'let ', 'var ', '=>']):
        return 'javascript'
    
    # Java indicators
    if any(keyword in code for keyword in ['public class', 'private ', 'public static void main']):
        return 'java'
    
    # C++ indicators
    if any(keyword in code for keyword in ['#include', 'std::', 'cout', 'cin']):
        return 'cpp'
    
    # C indicators
    if any(keyword in code for keyword in ['#include', 'printf', 'scanf', 'main(']):
        return 'c'
    
    return 'unknown'

def log_analysis_request(client_ip: str, code_length: int, analysis_type: str):
    """Log analysis request for monitoring"""
    logger.info(f"Analysis request - IP: {client_ip}, Code length: {code_length}, Type: {analysis_type}")

def create_error_response(message: str, code: int = 400) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error": message,
        "status_code": code,
        "timestamp": time.time()
    }

def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "success": True,
        "data": data,
        "timestamp": time.time()
    }

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, client_id: str, max_requests: int = 30, window_seconds: int = 60) -> bool:
        """Check if request is allowed"""
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < window_seconds
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(current_time)
        return True

def benchmark_function(func):
    """Decorator to benchmark function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"Function {func.__name__} took {end_time - start_time:.3f} seconds")
        return result
    
    return wrapper

def chunk_code(code: str, max_chunk_size: int = 1000) -> List[str]:
    """Split large code into smaller chunks for processing"""
    if len(code) <= max_chunk_size:
        return [code]
    
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in lines:
        line_size = len(line) + 1  # +1 for newline
        
        if current_size + line_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def escape_html(text: str) -> str:
    """Escape HTML characters"""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&#x27;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_url(url: str) -> bool:
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

# Global rate limiter instance
rate_limiter = RateLimiter()
