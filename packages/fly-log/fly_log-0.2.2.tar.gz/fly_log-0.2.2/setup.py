from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf8") 

setup(
    name = 'fly_log',
    version = '0.2.2', 
    keywords='fly log debug',
    description = 'a simple log for small project',    
    long_description=long_description,
    long_description_content_type='text/markdown', 
    license = 'MIT License',
    url = 'https://github.com/zero-space-man-community/fly_log',
    author = 'flythinker',
    author_email = 'flythinker@qq.com',
    # packages = find_packages(),
    packages=['fly_log'],
    package_dir={'fly_log':'fly_log'},
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
      ],
)