from PySide2 import QtWidgets, QtWebEngineWidgets
import sys
import os
import misaka as m

class MathHTMLRenderer(m.HtmlRenderer):
    # disable codespan for AsciiMath to read math
    def codespan(self, text):
        pass

class Editor(QtWidgets.QWidget):
    def __init__(self):
        super(Editor, self).__init__()
        self.setWindowTitle("AsciiMathMarkdown")
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.layout = QtWidgets.QHBoxLayout()
        self.entry = QtWidgets.QTextEdit()
        self.entry.setAcceptRichText(False)
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setEnabled(False)
        self.layout.addWidget(self.entry, 50)
        self.layout.addWidget(self.browser, 50)
        self.entry.textChanged.connect(self.update_webview)
        self.topbar = QtWidgets.QMenuBar(self)
        self.vlayout.addWidget(self.topbar)
        self.vlayout.addLayout(self.layout)
        self.export = QtWidgets.QAction("Export", self)
        self.export.setShortcut('Ctrl+E')
        self.export.setStatusTip("Export to a PDF")
        self.export.triggered.connect(self.export_pdf)
        self.topbar.addAction(self.export)

    def export_pdf(self):
        path, _ = self.dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as...', filter='PDF files (*.pdf)')
        if path:
            self.browser.page().printToPdf(path)

    def update_webview(self):
        renderer = MathHTMLRenderer()
        mi = m.Markdown(renderer)
        html = mi(self.entry.toPlainText())
        html = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>' \
               + html + '</body>'
        self.browser.setHtml(html)

def main(*args):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    win = Editor()
    win.showMaximized()
    sys.exit(app.exec_())

main()