from distutils.core import setup

dependencies = (
    'numpy', 'numba', 'matplotlib', 'imageio', 'imageio-ffmpeg'
)

packages = ['', '.config', '.obj', '.utils']
for n, package in enumerate(packages):
    packages[n] = 'gridvid' + package

url = 'https://github.com/GabrielSCabrera/Gridvid'
setup(
    name = 'Gridvid',
    packages = packages,
    version = '0.0.1',
    description = 'Allows you to put various grids on videos.',
    author = 'Gabriel S. Cabrera',
    author_email = 'gabriel.sigurd.cabrera@gmail.com',
    url = url,
    download_url = url + 'archive/v0.0.1.tar.gz',
    keywords = ['grid', 'video', 'overlay'],
    install_requires = dependencies,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.8'
    ],
)
