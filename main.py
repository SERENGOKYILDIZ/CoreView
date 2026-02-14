import sys
import os
import markdown2
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtGui import QAction, QIcon
from config import APP_NAME, VERSION

class MarkdownViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.current_path = None
        
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(1100, 850)
        
        # Logo Ayarı
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Performans Ayarı (Bellek dostu)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        
        self.create_menus()
        
        # Başlangıç dosyası (CLI / Birlikte Aç)
        if len(sys.argv) > 1:
            self.load_file(" ".join(sys.argv[1:]))
        else:
            self.update_view()

        self.showMaximized()

    def get_css(self):
        is_dark = self.is_dark_mode
        bg = "#0d1117" if is_dark else "#ffffff"
        fg = "#c9d1d9" if is_dark else "#1f2328"
        border = "#30363d" if is_dark else "#d0d7de"
        link = "#58a6ff" if is_dark else "#0969da"
        inline_bg = "rgba(110, 118, 129, 0.4)" if is_dark else "rgba(175, 184, 193, 0.2)"
        
        return f"""
        body {{ 
            background-color: {bg}; color: {fg}; 
            font-family: -apple-system, Segoe UI, sans-serif; 
            padding: 45px; line-height: 1.6; font-size: 16px;
        }}
        h1, h2 {{ border-bottom: 1px solid {border}; padding-bottom: 8px; }}
        a {{ color: {link}; text-decoration: none; }}
        code {{ background-color: {inline_bg}; padding: .2em .4em; border-radius: 6px; font-family: monospace; }}
        pre {{ background-color: #161b22; color: #e6edf3; padding: 16px; border-radius: 8px; overflow: auto; border: 1px solid {border}; }}
        pre code {{ background-color: transparent; color: inherit; }}
        """

    def update_view(self, md_content=None):
        md_text = md_content if md_content else f"# {APP_NAME}\nHoş geldiniz. Dosya açmak için **Dosya > Aç** kullanın."
        html_body = markdown2.markdown(md_text, extras=["fenced-code-blocks", "tables", "break-on-newline", "header-ids"])
        full_html = f"<html><head><meta charset='UTF-8'><style id='main-style'>{self.get_css()}</style></head><body>{html_body}</body></html>"
        self.browser.setHtml(full_html)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        css = self.get_css().replace("\n", " ")
        js = f"document.getElementById('main-style').innerHTML = `{css}`;"
        self.browser.page().runJavaScript(js)

    def load_file(self, path):
        path = path.strip('"').strip("'")
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.current_path = path
            self.update_view(content)
            self.setWindowTitle(f"{APP_NAME} - {os.path.basename(path)}")
        except Exception as e:
            print(f"Hata: {e}")

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Dosya")
        open_act = QAction("Aç", self)
        open_act.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_act)
        
        view_menu = menubar.addMenu("Görünüm")
        theme_act = QAction("Temayı Değiştir", self)
        theme_act.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_act)

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seç", "", "Markdown (*.md)")
        if path: self.load_file(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownViewer()
    window.show()
    sys.exit(app.exec())