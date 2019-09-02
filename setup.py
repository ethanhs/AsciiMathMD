from distutils.core import setup
import py2exe

setup(
    name='AsciiMathMD',
    version='0.1.0',
    author='Ethan Smith',
    author_email='ethanhs@berkeley.edu',
    description= ('A text editor that renders and exports AsciiMath and Markdown'),
    license='GPL v3.0',
    install_requires=['PySide2', 'misaka'],
    entry_points={'gui_scripts':
                 ['AsciiMathMD = AsciiMathMD:main']}

)