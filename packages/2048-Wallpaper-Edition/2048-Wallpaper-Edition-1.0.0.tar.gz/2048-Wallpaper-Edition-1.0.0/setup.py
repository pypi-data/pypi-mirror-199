from setuptools import setup, find_packages

setup(
    name='2048-Wallpaper-Edition',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Pillow==8.4.0',
        'keyboard==0.13.5',
    ],
    entry_points={
        'console_scripts': [
            '2048-Wallpaper-Edition = 2048.2048:main',
        ],
    },
)
