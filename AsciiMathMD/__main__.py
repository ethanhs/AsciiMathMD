from PySide2 import QtWidgets, QtWebEngineWidgets
import sys
import os
import misaka as m
import pathlib

class MathHTMLRenderer(m.HtmlRenderer):
    # disable codespan for AsciiMath to read math
    def codespan(self, text):
        pass

class Editor(QtWidgets.QWidget):
    def __init__(self, path = None):
        super(Editor, self).__init__()
        self.setWindowTitle("AsciiMathMarkdown")
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.layout = QtWidgets.QHBoxLayout()
        self.entry = QtWidgets.QTextEdit()
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setEnabled(False)
        self.browser.setZoomFactor(0.7)
        if path is not None:
            with open(path) as f:
                for line in f.readlines():
                    self.entry.append(line.replace('\n', ''))
            self.update_webview()
        self.entry.setAcceptRichText(False)
        self.layout.addWidget(self.entry, 50)
        self.layout.addWidget(self.browser, 50)
        self.entry.textChanged.connect(self.update_webview)
        self.topbar = QtWidgets.QMenuBar(self)
        self.vlayout.addWidget(self.topbar)
        self.vlayout.addLayout(self.layout)
        self.export = QtWidgets.QAction("Export", self)
        self.export.setShortcut('Ctrl+E')
        self.export.setStatusTip("Export to a PDF")
        self.save = QtWidgets.QAction("Save", self)
        self.save.setShortcut('Ctrl+S')
        self.save.setStatusTip("Save Markdown")
        self.save.triggered.connect(self.save_markdown)
        self.export.triggered.connect(self.export_pdf)
        self.topbar.addAction(self.save)
        self.topbar.addAction(self.export)

    def export_pdf(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export as...', filter='PDF files (*.pdf)')
        if path:
            self.browser.page().printToPdf(path)

    def save_markdown(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as...', filter='Markdown files (*.md)')
        if path:
            with open(path, 'w') as f:
                f.write(self.entry.toPlainText())

    def update_webview(self):
        renderer = MathHTMLRenderer()
        mi = m.Markdown(renderer)
        html = mi(self.entry.toPlainText())
        html = '<body><script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>' \
               + html + '</body>'
        self.browser.setHtml(html)

def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) == 2:
        path = pathlib.Path(sys.argv[1])
        win = Editor(path)
    else:
        win = Editor()
    win.showMaximized()
    sys.exit(app.exec_())

main()