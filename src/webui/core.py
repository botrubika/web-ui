import subprocess
import platform
import requests
from ping3 import ping
from typing import Dict, List, Optional
from datetime import datetime
import socket
import re


class WebMonitor:
    """کلاس اصلی برای مانیتورینگ و تست امنیتی وب‌سایت‌ها"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.results = {}
    
    def ping_host(self, host: str) -> Dict:
        """
        بررسی پینگ یک هاست
        """
        try:
            # حذف پروتکل از آدرس
            clean_host = re.sub(r'^https?://', '', host)
            clean_host = clean_host.split('/')[0]
            
            response_time = ping(clean_host, timeout=self.timeout)
            
            if response_time is not None:
                return {
                    "status": "✅ موفق",
                    "response_time": f"{response_time * 1000:.2f} ms",
                    "message": "هاست در دسترس است"
                }
            else:
                return {
                    "status": "❌ ناموفق",
                    "response_time": "N/A",
                    "message": "درخواست منقضی شد"
                }
        except Exception as e:
            return {
                "status": "⚠️ خطا",
                "response_time": "N/A",
                "message": f"خطا: {str(e)}"
            }
    
    def check_http_status(self, url: str) -> Dict:
        """
        بررسی وضعیت HTTP و امنیت وب‌سایت
        """
        try:
            # اضافه کردن پروتکل اگر نبود
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.get(url, timeout=self.timeout, allow_redirects=True)
            
            security_headers = self._check_security_headers(response.headers)
            security_score = self._calculate_security_score(security_headers)
            
            return {
                "status": "✅ سالم" if 200 <= response.status_code < 400 else "⚠️ هشدار",
                "status_code": response.status_code,
                "response_time": f"{response.elapsed.total_seconds() * 1000:.2f} ms",
                "security_headers": security_headers,
                "security_score": f"{security_score}/5",
                "server": response.headers.get('Server', 'نامشخص'),
                "message": f"HTTP {response.status_code}"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "❌ خطا",
                "status_code": "N/A",
                "message": "ارتباط برقرار نشد - سایت ممکن است下线 باشد"
            }
        except requests.exceptions.Timeout:
            return {
                "status": "❌ خطا",
                "status_code": "N/A",
                "message": "مهلت درخواست تمام شد"
            }
        except Exception as e:
            return {
                "status": "⚠️ خطا",
                "status_code": "N/A",
                "message": f"خطا: {str(e)}"
            }
    
    def _check_security_headers(self, headers: Dict) -> Dict:
        """بررسی هدرهای امنیتی مهم"""
        security_checks = {
            "Strict-Transport-Security (HSTS)": headers.get('Strict-Transport-Security', '❌ وجود ندارد'),
            "Content-Security-Policy (CSP)": headers.get('Content-Security-Policy', '❌ وجود ندارد'),
            "X-Frame-Options": headers.get('X-Frame-Options', '❌ وجود ندارد'),
            "X-Content-Type-Options": headers.get('X-Content-Type-Options', '❌ وجود ندارد'),
            "Referrer-Policy": headers.get('Referrer-Policy', '❌ وجود ندارد'),
        }
        return security_checks
    
    def _calculate_security_score(self, security_headers: Dict) -> int:
        """محاسبه امتیاز امنیتی از ۰ تا ۵"""
        score = 0
        for header, value in security_headers.items():
            if '❌ وجود ندارد' not in value:
                score += 1
        return score
    
    def check_dns_resolution(self, domain: str) -> Dict:
        """بررسی رزولوشن DNS"""
        try:
            clean_domain = re.sub(r'^https?://', '', domain)
            clean_domain = clean_domain.split('/')[0]
            
            ip = socket.gethostbyname(clean_domain)
            return {
                "status": "✅ موفق",
                "ip": ip,
                "message": f"DNS resolved successfully"
            }
        except socket.gaierror:
            return {
                "status": "❌ ناموفق",
                "ip": "N/A",
                "message": "DNS resolution failed"
            }
    
    def full_scan(self, target: str) -> Dict:
        """اسکن کامل یک وب‌سایت"""
        result = {
            "target": target,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ping": self.ping_host(target),
            "http": self.check_http_status(target),
            "dns": self.check_dns_resolution(target)
        }
        return result
