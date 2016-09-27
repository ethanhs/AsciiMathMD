from distutils.core import setup
import py2exe

setup(
    name='AsciiMathMD',
    version='0.0.1',
    author='Ethan Smith',
    author_email='ethanhs@berkeley.edu',
    description= ('A text editor that renders and exports AsciiMath and Markdown'),
    license='GPL v3.0',
    install_requires=['PyQt5', 'misaka'],
    entry_points={'gui_scripts':
                 ['AsciiMathMD = AsciiMathMD:main']}

)