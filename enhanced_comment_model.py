"""
Enhanced Code Analysis and Documentation Platform
Advanced AI-powered code commenting, analysis, and documentation generation
"""

import ast
import re
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time
from langdetect import detect
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from transformers import pipeline
import openai
from config import Config

class CodeLanguage(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    TYPESCRIPT = "typescript"
    PHP = "php"
    RUBY = "ruby"
    GO = "go"
    RUST = "rust"
    SWIFT = "swift"
    UNKNOWN = "unknown"

@dataclass
class CodeAnalysisResult:
    """Result of code analysis"""
    commented_code: str
    language: str
    complexity_score: float
    security_issues: List[Dict[str, Any]]
    performance_suggestions: List[str]
    code_quality_score: float
    documentation_generated: str
    function_signatures: List[str]
    class_definitions: List[str]
    imports_used: List[str]
    lines_of_code: int
    cyclomatic_complexity: int

class AdvancedCommentGenerator:
    """Advanced AI-powered code comment and documentation generator"""
    
    def __init__(self):
        self.config = Config()
        self.comment_generator = None
        self.openai_client = None
        self._init_models()
    
    def _init_models(self):
        """Initialize AI models"""
        try:
            # Initialize Transformers model
            if self.config.DEFAULT_MODEL:
                self.comment_generator = pipeline(
                    'text2text-generation', 
                    model=self.config.DEFAULT_MODEL,
                    max_length=512,
                    temperature=0.7
                )
        except Exception as e:
            print(f"Warning: Could not initialize transformers model: {e}")
        
        # Initialize OpenAI if API key is available
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
            self.openai_client = openai
    
    def detect_language(self, code: str) -> CodeLanguage:
        """Detect programming language from code"""
        try:
            lexer = guess_lexer(code)
            language_name = lexer.name.lower()
            
            language_mapping = {
                'python': CodeLanguage.PYTHON,
                'javascript': CodeLanguage.JAVASCRIPT,
                'java': CodeLanguage.JAVA,
                'c++': CodeLanguage.CPP,
                'c': CodeLanguage.C,
                'typescript': CodeLanguage.TYPESCRIPT,
                'php': CodeLanguage.PHP,
                'ruby': CodeLanguage.RUBY,
                'go': CodeLanguage.GO,
                'rust': CodeLanguage.RUST,
                'swift': CodeLanguage.SWIFT
            }
            
            for key, lang in language_mapping.items():
                if key in language_name:
                    return lang
                    
            return CodeLanguage.UNKNOWN
            
        except Exception:
            return CodeLanguage.UNKNOWN
    
    def analyze_python_code(self, code: str) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code)
            
            functions = []
            classes = []
            imports = []
            complexity = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(f"{node.name}({', '.join(arg.arg for arg in node.args.args)})")
                    complexity += self._calculate_complexity(node)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend(alias.name for alias in node.names)
                    else:
                        imports.append(node.module or "")
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'complexity': complexity,
                'lines': len(code.split('\n'))
            }
        except Exception as e:
            print(f"Error analyzing Python code: {e}")
            return {'functions': [], 'classes': [], 'imports': [], 'complexity': 0, 'lines': 0}
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                                ast.With, ast.AsyncWith, ast.Try, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    def generate_smart_comments(self, code: str, language: CodeLanguage) -> str:
        """Generate intelligent comments based on code analysis"""
        
        if language == CodeLanguage.PYTHON:
            return self._generate_python_comments(code)
        elif language == CodeLanguage.JAVASCRIPT:
            return self._generate_javascript_comments(code)
        else:
            return self._generate_generic_comments(code, language.value)
    
    def _generate_python_comments(self, code: str) -> str:
        """Generate Python-specific comments"""
        lines = code.split('\n')
        commented_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            # Skip empty lines and existing comments
            if not stripped or stripped.startswith('#'):
                commented_lines.append(line)
                continue
            
            comment = self._get_python_line_comment(stripped)
            
            if comment:
                commented_lines.append(' ' * indent + f"# {comment}")
                commented_lines.append(line)
            else:
                commented_lines.append(line)
        
        return '\n'.join(commented_lines)
    
    def _get_python_line_comment(self, line: str) -> str:
        """Get appropriate comment for a Python line"""
        patterns = {
            r'^import\s+(.+)': lambda m: f"Import {m.group(1)} module",
            r'^from\s+(.+)\s+import\s+(.+)': lambda m: f"Import {m.group(2)} from {m.group(1)}",
            r'^def\s+(\w+)\s*\(': lambda m: f"Define function {m.group(1)}",
            r'^class\s+(\w+)': lambda m: f"Define class {m.group(1)}",
            r'^if\s+': lambda m: "Conditional statement",
            r'^elif\s+': lambda m: "Alternative condition",
            r'^else\s*:': lambda m: "Default case",
            r'^for\s+': lambda m: "Loop iteration",
            r'^while\s+': lambda m: "While loop",
            r'^try\s*:': lambda m: "Exception handling block",
            r'^except\s+': lambda m: "Handle specific exception",
            r'^finally\s*:': lambda m: "Cleanup code",
            r'^with\s+': lambda m: "Context manager",
            r'^return\s+': lambda m: "Return value from function",
            r'^print\s*\(': lambda m: "Output to console",
            r'(\w+)\s*=\s*(.+)': lambda m: f"Assign value to {m.group(1)}",
        }
        
        for pattern, comment_func in patterns.items():
            match = re.match(pattern, line)
            if match:
                return comment_func(match)
        
        return ""
    
    def _generate_javascript_comments(self, code: str) -> str:
        """Generate JavaScript-specific comments"""
        lines = code.split('\n')
        commented_lines = []
        
        for line in lines:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            if not stripped or stripped.startswith('//') or stripped.startswith('/*'):
                commented_lines.append(line)
                continue
            
            comment = self._get_javascript_line_comment(stripped)
            
            if comment:
                commented_lines.append(' ' * indent + f"// {comment}")
                commented_lines.append(line)
            else:
                commented_lines.append(line)
        
        return '\n'.join(commented_lines)
    
    def _get_javascript_line_comment(self, line: str) -> str:
        """Get appropriate comment for a JavaScript line"""
        patterns = {
            r'^function\s+(\w+)\s*\(': lambda m: f"Define function {m.group(1)}",
            r'^const\s+(\w+)\s*=': lambda m: f"Declare constant {m.group(1)}",
            r'^let\s+(\w+)\s*=': lambda m: f"Declare variable {m.group(1)}",
            r'^var\s+(\w+)\s*=': lambda m: f"Declare variable {m.group(1)}",
            r'^if\s*\(': lambda m: "Conditional statement",
            r'^else\s+if\s*\(': lambda m: "Alternative condition",
            r'^else\s*{': lambda m: "Default case",
            r'^for\s*\(': lambda m: "For loop",
            r'^while\s*\(': lambda m: "While loop",
            r'^try\s*{': lambda m: "Exception handling block",
            r'^catch\s*\(': lambda m: "Handle exception",
            r'^finally\s*{': lambda m: "Cleanup code",
            r'^return\s+': lambda m: "Return value",
            r'^console\.log\s*\(': lambda m: "Log to console",
            r'^import\s+': lambda m: "Import module",
            r'^export\s+': lambda m: "Export module/function",
        }
        
        for pattern, comment_func in patterns.items():
            match = re.match(pattern, line)
            if match:
                return comment_func(match)
        
        return ""
    
    def _generate_generic_comments(self, code: str, language: str) -> str:
        """Generate generic comments for other languages"""
        if self.openai_client:
            return self._generate_ai_comments(code, language)
        elif self.comment_generator:
            return self._generate_transformer_comments(code, language)
        else:
            return self._generate_basic_comments(code)
    
    def _generate_ai_comments(self, code: str, language: str) -> str:
        """Generate comments using OpenAI API"""
        try:
            prompt = f"""
            Add meaningful comments to this {language} code. 
            Make the comments helpful and explain what each section does.
            Preserve the original code structure and indentation.
            
            Code:
            {code}
            """
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return self._generate_basic_comments(code)
    
    def _generate_transformer_comments(self, code: str, language: str) -> str:
        """Generate comments using Transformers model"""
        try:
            prompt = f"Add comments to this {language} code:\n{code}"
            result = self.comment_generator(prompt, max_length=512, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            print(f"Error with transformer model: {e}")
            return self._generate_basic_comments(code)
    
    def _generate_basic_comments(self, code: str) -> str:
        """Generate basic comments as fallback"""
        return f"# Generated comments for code\n{code}"
    
    def check_security_issues(self, code: str, language: CodeLanguage) -> List[Dict[str, Any]]:
        """Check for common security issues"""
        issues = []
        
        security_patterns = {
            'SQL Injection': [
                r'execute\s*\(\s*["\'].*%.*["\']',
                r'query\s*\(\s*["\'].*\+.*["\']',
            ],
            'XSS Vulnerability': [
                r'innerHTML\s*=\s*.*\+',
                r'document\.write\s*\(',
            ],
            'Hardcoded Credentials': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
            ],
            'Unsafe File Operations': [
                r'open\s*\(\s*.*\+',
                r'exec\s*\(',
                r'eval\s*\(',
            ]
        }
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            for issue_type, patterns in security_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            'type': issue_type,
                            'line': line_num,
                            'code': line.strip(),
                            'severity': 'high' if 'injection' in issue_type.lower() else 'medium'
                        })
        
        return issues
    
    def analyze_performance(self, code: str, language: CodeLanguage) -> List[str]:
        """Analyze code for performance issues"""
        suggestions = []
        
        performance_patterns = {
            'Nested loops detected - consider optimization': r'for.*:\s*\n.*for.*:',
            'Global variables used - consider local scope': r'^global\s+\w+',
            'Inefficient string concatenation': r'\w+\s*\+=\s*["\']',
            'Repeated function calls in loop': r'for.*:\s*\n.*\w+\(.*\)',
            'Large list comprehension - consider generator': r'\[.*for.*in.*for.*in.*\]',
        }
        
        for suggestion, pattern in performance_patterns.items():
            if re.search(pattern, code, re.MULTILINE):
                suggestions.append(suggestion)
        
        return suggestions
    
    def calculate_quality_score(self, code: str, analysis: Dict[str, Any]) -> float:
        """Calculate code quality score"""
        score = 100.0
        
        # Deduct points for complexity
        if analysis.get('complexity', 0) > 10:
            score -= min(20, analysis['complexity'] - 10)
        
        # Deduct points for long functions (if detectable)
        lines = len(code.split('\n'))
        if lines > 100:
            score -= min(15, (lines - 100) / 10)
        
        # Deduct points for lack of comments
        comment_ratio = len(re.findall(r'#|//|/\*', code)) / max(lines, 1)
        if comment_ratio < 0.1:
            score -= 10
        
        return max(0, score)
    
    def generate_documentation(self, code: str, analysis: Dict[str, Any], language: CodeLanguage) -> str:
        """Generate comprehensive documentation"""
        doc = f"""
# Code Documentation

## Overview
- **Language**: {language.value.title()}
- **Lines of Code**: {analysis.get('lines', 'N/A')}
- **Complexity Score**: {analysis.get('complexity', 'N/A')}

## Functions
{chr(10).join(f"- {func}" for func in analysis.get('functions', []))}

## Classes
{chr(10).join(f"- {cls}" for cls in analysis.get('classes', []))}

## Dependencies
{chr(10).join(f"- {imp}" for imp in analysis.get('imports', []))}

## Generated at
{time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        return doc.strip()
    
    def comprehensive_analysis(self, code: str) -> CodeAnalysisResult:
        """Perform comprehensive code analysis"""
        language = self.detect_language(code)
        
        # Language-specific analysis
        if language == CodeLanguage.PYTHON:
            analysis = self.analyze_python_code(code)
        else:
            analysis = {'functions': [], 'classes': [], 'imports': [], 'complexity': 0, 'lines': len(code.split('\n'))}
        
        # Generate commented code
        commented_code = self.generate_smart_comments(code, language)
        
        # Security analysis
        security_issues = []
        if self.config.ENABLE_SECURITY_SCAN:
            security_issues = self.check_security_issues(code, language)
        
        # Performance analysis
        performance_suggestions = []
        if self.config.ENABLE_PERFORMANCE_ANALYSIS:
            performance_suggestions = self.analyze_performance(code, language)
        
        # Quality score
        quality_score = self.calculate_quality_score(code, analysis)
        
        # Documentation
        documentation = self.generate_documentation(code, analysis, language)
        
        return CodeAnalysisResult(
            commented_code=commented_code,
            language=language.value,
            complexity_score=analysis.get('complexity', 0),
            security_issues=security_issues,
            performance_suggestions=performance_suggestions,
            code_quality_score=quality_score,
            documentation_generated=documentation,
            function_signatures=analysis.get('functions', []),
            class_definitions=analysis.get('classes', []),
            imports_used=analysis.get('imports', []),
            lines_of_code=analysis.get('lines', 0),
            cyclomatic_complexity=analysis.get('complexity', 0)
        )

# Global instance
comment_generator = AdvancedCommentGenerator()

def generate_comment(code: str) -> str:
    """Main function for generating comments (backward compatibility)"""
    try:
        result = comment_generator.comprehensive_analysis(code)
        return result.commented_code
    except Exception as e:
        print(f"Error generating comment: {e}")
        return f"# Error generating comments\n{code}"

def analyze_code(code: str) -> Dict[str, Any]:
    """Comprehensive code analysis function"""
    try:
        result = comment_generator.comprehensive_analysis(code)
        return {
            'commented_code': result.commented_code,
            'language': result.language,
            'complexity_score': result.complexity_score,
            'security_issues': result.security_issues,
            'performance_suggestions': result.performance_suggestions,
            'code_quality_score': result.code_quality_score,
            'documentation': result.documentation_generated,
            'function_signatures': result.function_signatures,
            'class_definitions': result.class_definitions,
            'imports_used': result.imports_used,
            'lines_of_code': result.lines_of_code,
            'cyclomatic_complexity': result.cyclomatic_complexity
        }
    except Exception as e:
        print(f"Error in code analysis: {e}")
        return {
            'commented_code': f"# Error in analysis\n{code}",
            'language': 'unknown',
            'error': str(e)
        }
