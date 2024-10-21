from setuptools import setup, find_packages

setup(
    name="risk_assessment",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'streamlit',
        'python-docx',
        'joblib'
        'setuptools',
        'fpdf'
    ],
)