from distutils.core import setup, Extension

module1 = Extension("sherlock", ["sherlockmodule.c", "sherlock.c"])

setup(
    name='sherlock',
    version='1.0',
    description='Plagiarism detection algorithm',
    url='http://sydney.edu.au/engineering/it/~scilect/sherlock/',
    author='Rob Pike',
    ext_modules=[module1],
    include_dirs='',
    py_modules=['']
)