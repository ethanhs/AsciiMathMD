from PyQt5 import QtWidgets, QtWebEngineWidgets
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
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 30, 0, 0)
        self.entry = QtWidgets.QTextEdit()
        self.entry.setAcceptRichText(False)
        self.entry.resize(self.window().width()//2, self.window().height())
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setEnabled(False)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.browser)
        self.entry.textChanged.connect(self.update_webview)
        self.topbar = QtWidgets.QMenuBar(self)
        self.topbar.setFixedSize(60, 30)
        self.export = QtWidgets.QAction("Export", self)
        self.export.setShortcut('Ctrl+E')
        self.export.setStatusTip("Export to a PDF")
        self.export.triggered.connect(self.export_pdf)
        self.topbar.addAction(self.export)

    def export_pdf(self):
        self.dialog = QtWidgets.QDialog(self)
        self.dialog.setWindowTitle('Save as...')
        self.lay = QtWidgets.QVBoxLayout(self.dialog)
        self.lay2 = QtWidgets.QHBoxLayout()
        self.inp = QtWidgets.QLineEdit()
        self.ok = QtWidgets.QPushButton('OK')
        self.ok.resize(60,30)
        self.lay.addWidget(self.inp)
        self.lay.addWidget(self.ok)
        self.ok.clicked.connect(self.save)
        self.dialog.exec()

    def save(self):
        self.dialog.close()
        file_path = self.inp.text()
        if file_path:
            self.browser.page().printToPdf(file_path)

    def update_webview(self):
        renderer = MathHTMLRenderer()
        mi = m.Markdown(renderer)
        html = mi(self.entry.toPlainText())
        html = '<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML"></script>' \
               + html + '</body>'
        self.browser.setHtml(html)

def main(*args):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    win = Editor()
    win.showMaximized()
    sys.exit(app.exec_())

main()