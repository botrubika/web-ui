from flask import Flask, render_template, request, jsonify
from .core import WebMonitor
import json

app = Flask(__name__)
monitor = WebMonitor()

@app.route('/')
def index():
    """صفحه اصلی وب‌سایت"""
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    """API برای اسکن یک وب‌سایت"""
    data = request.get_json()
    target = data.get('target', '').strip()
    
    if not target:
        return jsonify({'error': 'لطفاً آدرس وب‌سایت را وارد کنید'}), 400
    
    # انجام اسکن کامل
    result = monitor.full_scan(target)
    
    return jsonify(result)

@app.route('/api/ping', methods=['POST'])
def ping_check():
    """API برای تست پینگ"""
    data = request.get_json()
    target = data.get('target', '').strip()
    
    if not target:
        return jsonify({'error': 'لطفاً آدرس را وارد کنید'}), 400
    
    result = monitor.ping_host(target)
    return jsonify(result)

@app.route('/api/http', methods=['POST'])
def http_check():
    """API برای بررسی HTTP و امنیت"""
    data = request.get_json()
    target = data.get('target', '').strip()
    
    if not target:
        return jsonify({'error': 'لطفاً آدرس وب‌سایت را وارد کنید'}), 400
    
    result = monitor.check_http_status(target)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
