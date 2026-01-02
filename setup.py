from setuptools import setup

setup(
    name='svd-editor',
    version='1.0.0',
    py_modules=['ww_svd_editor'],
    entry_points={
        'console_scripts': [
            'svd-editor=ww_svd_editor:main',
        ],
    },
    install_requires=[
        'pythonnet>=3.0.0'
    ],
    description='CLI tool to view/edit Unity ww.svd save files safely',
    author='Your Name',
    url='https://github.com/<your-username>/ww-svd-editor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
)
