/**
 * Advanced Code Analysis Interface
 * JavaScript functionality for the analysis page
 */

class CodeAnalyzer {
    constructor() {
        this.currentAnalysis = null;
        this.analysisType = 'full';
        this.qualityChart = null;
        this.initializeEventListeners();
        this.loadStatistics();
        this.setupFileUpload();
    }

    initializeEventListeners() {
        // Analysis option selection
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', () => {
                document.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                this.analysisType = card.dataset.type;
            });
        });

        // File input change
        document.getElementById('file-input').addEventListener('change', this.handleFileUpload.bind(this));

        // Code input auto-resize
        const codeInput = document.getElementById('code-input');
        codeInput.addEventListener('input', () => {
            this.autoResizeTextarea(codeInput);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                this.analyzeCode();
            }
        });
    }

    setupFileUpload() {
        const uploadArea = document.querySelector('.file-upload');
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.processFile(files[0]);
            }
        });
    }

    switchInputTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    switchResultTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.result-tab').forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');

        // Update tab content
        document.querySelectorAll('.result-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`${tabName}-content`).classList.add('active');
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(textarea.scrollHeight, 300) + 'px';
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('code-input').value = e.target.result;
            this.switchInputTab('paste');
            this.showNotification(`File "${file.name}" loaded successfully`, 'success');
        };
        reader.onerror = () => {
            this.showNotification('Error reading file', 'error');
        };
        reader.readAsText(file);
    }

    async fetchFromUrl() {
        const url = document.getElementById('url-input').value.trim();
        if (!url) {
            this.showNotification('Please enter a valid URL', 'error');
            return;
        }

        try {
            this.showLoading('Fetching code from URL...');
            
            // For GitHub URLs, convert to raw content URL
            let fetchUrl = url;
            if (url.includes('github.com') && url.includes('/blob/')) {
                fetchUrl = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/');
            }

            const response = await fetch(`/api/fetch-url`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: fetchUrl })
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            document.getElementById('code-input').value = data.content;
            this.switchInputTab('paste');
            this.showNotification('Code fetched successfully', 'success');
            
        } catch (error) {
            this.showNotification(`Failed to fetch code: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async analyzeCode() {
        const code = document.getElementById('code-input').value.trim();
        
        if (!code) {
            this.showNotification('Please enter some code to analyze', 'error');
            return;
        }

        try {
            this.showLoading('Analyzing your code...');
            this.updateLoadingProgress('Initializing analysis engine...');

            const startTime = Date.now();
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: code,
                    analysis_type: this.analysisType
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Analysis failed');
            }

            this.updateLoadingProgress('Processing results...');
            const result = await response.json();
            
            this.currentAnalysis = result;
            this.displayResults(result);
            this.updateAnalysisInfo(result);
            this.updateQualityChart(result);
            this.addToRecentActivity(result);
            
            const processingTime = (Date.now() - startTime) / 1000;
            this.showNotification(`Analysis completed in ${processingTime.toFixed(2)}s`, 'success');

        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification(`Analysis failed: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(result) {
        // Show results section
        document.getElementById('results-section').classList.add('active');

        // Display commented code
        if (result.commented_code) {
            document.getElementById('commented-code').textContent = result.commented_code;
            // Re-run Prism highlighting
            Prism.highlightAll();
        }

        // Display security issues
        this.displaySecurityIssues(result.security_issues || []);

        // Display performance suggestions
        this.displayPerformanceSuggestions(result.performance_suggestions || []);

        // Display documentation
        if (result.documentation) {
            document.getElementById('documentation-result').innerHTML = 
                this.formatDocumentation(result.documentation);
        }
    }

    displaySecurityIssues(issues) {
        const container = document.getElementById('security-issues');
        
        if (!issues || issues.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #4CAF50;">
                    <i class="fas fa-shield-alt" style="font-size: 48px; margin-bottom: 15px;"></i>
                    <h3>No Security Issues Found</h3>
                    <p>Your code appears to be secure!</p>
                </div>
            `;
            return;
        }

        const issuesHtml = issues.map(issue => `
            <div class="security-issue ${issue.severity}">
                <div class="issue-header">
                    <div class="issue-type">${issue.type}</div>
                    <div class="issue-severity">${issue.severity.toUpperCase()}</div>
                </div>
                <p><strong>Line ${issue.line}:</strong> ${issue.code}</p>
                <p style="margin-top: 10px; color: #666;">
                    ${this.getSecurityAdvice(issue.type)}
                </p>
            </div>
        `).join('');

        container.innerHTML = issuesHtml;
    }

    displayPerformanceSuggestions(suggestions) {
        const container = document.getElementById('performance-suggestions');
        
        if (!suggestions || suggestions.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #4CAF50;">
                    <i class="fas fa-tachometer-alt" style="font-size: 48px; margin-bottom: 15px;"></i>
                    <h3>Great Performance!</h3>
                    <p>No performance issues detected.</p>
                </div>
            `;
            return;
        }

        const suggestionsHtml = suggestions.map(suggestion => `
            <div class="performance-suggestion">
                <i class="fas fa-lightbulb" style="color: #38b2ac; margin-right: 10px;"></i>
                ${suggestion}
            </div>
        `).join('');

        container.innerHTML = suggestionsHtml;
    }

    formatDocumentation(documentation) {
        return documentation.replace(/\n/g, '<br>').replace(/##\s+(.+)/g, '<h3>$1</h3>');
    }

    updateAnalysisInfo(result) {
        document.getElementById('detected-language').textContent = 
            result.language ? result.language.charAt(0).toUpperCase() + result.language.slice(1) : 'Unknown';
        document.getElementById('lines-of-code').textContent = result.lines_of_code || '0';
        document.getElementById('complexity-score').textContent = 
            result.complexity_score ? result.complexity_score.toFixed(1) : '-';
        document.getElementById('quality-score').textContent = 
            result.code_quality_score ? result.code_quality_score.toFixed(1) + '/100' : '-';
        document.getElementById('processing-time').textContent = 
            result.processing_time ? result.processing_time.toFixed(2) + 's' : '-';
    }

    updateQualityChart(result) {
        const ctx = document.getElementById('quality-chart').getContext('2d');
        
        if (this.qualityChart) {
            this.qualityChart.destroy();
        }

        const qualityScore = result.code_quality_score || 0;
        const complexityScore = Math.max(0, 100 - (result.complexity_score || 0) * 5);
        const securityScore = Math.max(0, 100 - (result.security_issues?.length || 0) * 20);
        
        this.qualityChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Quality', 'Complexity', 'Security'],
                datasets: [{
                    data: [qualityScore, complexityScore, securityScore],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#36d1dc'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { size: 12 },
                            padding: 15
                        }
                    }
                }
            }
        });
    }

    addToRecentActivity(result) {
        const container = document.getElementById('recent-activity');
        const time = new Date().toLocaleTimeString();
        
        const activity = `
            <div style="padding: 10px 0; border-bottom: 1px solid #eee;">
                <strong>${time}</strong><br>
                <small>Analyzed ${result.language} code (${result.lines_of_code} lines)</small>
            </div>
        `;
        
        container.innerHTML = activity + container.innerHTML;
        
        // Keep only last 5 activities
        const activities = container.querySelectorAll('div');
        if (activities.length > 5) {
            activities[activities.length - 1].remove();
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch('/api/statistics');
            const stats = await response.json();
            
            document.getElementById('total-analyses').textContent = 
                stats.total_analyses?.toLocaleString() || '-';
            document.getElementById('languages-supported').textContent = 
                stats.languages_supported || '-';
            document.getElementById('avg-processing-time').textContent = 
                stats.average_processing_time || '-';
            document.getElementById('security-issues-found').textContent = 
                stats.security_issues_found?.toLocaleString() || '-';
                
        } catch (error) {
            console.error('Failed to load statistics:', error);
        }
    }

    async exportReport(format) {
        if (!this.currentAnalysis) {
            this.showNotification('No analysis results to export', 'error');
            return;
        }

        try {
            const response = await fetch('/api/export-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    analysis_result: this.currentAnalysis,
                    format: format
                })
            });

            if (!response.ok) {
                throw new Error('Export failed');
            }

            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `code_analysis_report.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showNotification(`Report exported as ${format.toUpperCase()}`, 'success');

        } catch (error) {
            this.showNotification(`Export failed: ${error.message}`, 'error');
        }
    }

    shareResults() {
        if (!this.currentAnalysis) {
            this.showNotification('No analysis results to share', 'error');
            return;
        }

        const shareData = {
            title: 'Code Analysis Results',
            text: `My code analysis: ${this.currentAnalysis.language} code with quality score ${this.currentAnalysis.code_quality_score?.toFixed(1)}/100`,
            url: window.location.href
        };

        if (navigator.share) {
            navigator.share(shareData);
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(`${shareData.text} - ${shareData.url}`);
            this.showNotification('Results copied to clipboard', 'success');
        }
    }

    copyResult(elementId) {
        const element = document.getElementById(elementId);
        const text = element.textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Copied to clipboard', 'success');
        }).catch(() => {
            this.showNotification('Failed to copy', 'error');
        });
    }

    loadExample() {
        const exampleCode = `def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")

# Performance issue: recursive approach is inefficient
# Security issue: no input validation
`;
        
        document.getElementById('code-input').value = exampleCode;
        this.switchInputTab('paste');
        this.showNotification('Example code loaded', 'success');
    }

    clearAll() {
        document.getElementById('code-input').value = '';
        document.getElementById('url-input').value = '';
        document.getElementById('results-section').classList.remove('active');
        this.currentAnalysis = null;
        this.showNotification('Interface cleared', 'success');
    }

    showLoading(message) {
        document.getElementById('loading-overlay').style.display = 'flex';
        document.querySelector('.loading-content h3').textContent = message;
    }

    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
    }

    updateLoadingProgress(message) {
        document.getElementById('loading-progress').textContent = message;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 500;
            z-index: 10001;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
        `;
        
        // Set color based on type
        const colors = {
            success: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
            error: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
            info: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)'
        };
        
        notification.style.background = colors[type] || colors.info;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    getSecurityAdvice(issueType) {
        const advice = {
            'SQL Injection': 'Use parameterized queries or prepared statements to prevent SQL injection attacks.',
            'XSS Vulnerability': 'Sanitize user input and use proper encoding when displaying dynamic content.',
            'Hardcoded Credentials': 'Store sensitive data in environment variables or secure configuration files.',
            'Unsafe File Operations': 'Validate file paths and use safe file operation methods.'
        };
        
        return advice[issueType] || 'Review this code for potential security implications.';
    }
}

// Global functions for HTML onclick handlers
let analyzer;

function switchInputTab(tabName) {
    analyzer.switchInputTab(tabName);
}

function switchResultTab(tabName) {
    analyzer.switchResultTab(tabName);
}

function analyzeCode() {
    analyzer.analyzeCode();
}

function clearAll() {
    analyzer.clearAll();
}

function loadExample() {
    analyzer.loadExample();
}

function fetchFromUrl() {
    analyzer.fetchFromUrl();
}

function copyResult(elementId) {
    analyzer.copyResult(elementId);
}

function exportReport(format) {
    analyzer.exportReport(format);
}

function shareResults() {
    analyzer.shareResults();
}

// Initialize the analyzer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    analyzer = new CodeAnalyzer();
});

// Add some CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);
