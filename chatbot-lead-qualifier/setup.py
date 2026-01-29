from setuptools import setup, find_packages

setup(
    name='chatbot-lead-qualifier',
    version='1.0.0',
    description='Sistema de chatbot inteligente para calificar clientes potenciales',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'Flask==2.3.0',
        'Flask-CORS==4.0.0',
        'SQLAlchemy==2.0.0',
        'requests==2.31.0',
        'nltk==3.8.1',
        'transformers==4.30.0',
        'scikit-learn==1.3.0',
    ],
)
