"""
Web-UI - ابزار تست امنیت و در دسترس بودن وب‌سایت‌ها
"""

from .core import WebMonitor
from .app import app

__version__ = "0.1.0"
__all__ = ['WebMonitor', 'app']
