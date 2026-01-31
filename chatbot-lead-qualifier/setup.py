"""
Setup configuration for Chatbot Sparks IoT&Energy
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#') and not line.startswith('=')
        ]

setup(
    name='chatbot-sparks-energy',
    version='1.0.0',
    description='Sistema de chatbot inteligente para calificacion de leads en energia renovable',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sparks IoT&Energy',
    author_email='info@sparksenergy.io',
    url='https://sparksenergy.io',
    license='MIT',
    packages=find_packages(exclude=['tests', 'docs', 'deployment']),
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'prod': [
            'gunicorn>=21.0.0',
            'psycopg2-binary>=2.9.0',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Flask',
        'Topic :: Communications :: Chat',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    ],
    keywords='chatbot lead-qualification renewable-energy flask conversational-ai',
    project_urls={
        'Documentation': 'https://github.com/sparks-energy/chatbot-lead-qualifier',
        'Source': 'https://github.com/sparks-energy/chatbot-lead-qualifier',
        'Tracker': 'https://github.com/sparks-energy/chatbot-lead-qualifier/issues',
    },
    entry_points={
        'console_scripts': [
            'chatbot-sparks=run:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
