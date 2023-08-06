from setuptools import setup, find_packages

setup(
    name="eeg-pll",
    packages=find_packages(),
    version="1.10.0",
    license="MIT",
    description="PLL-Emotion-EEG - Pytorch",
    author="Guangyi Zhang",
    author_email="guangyi.zhang@utoronto.ca",
    url="https://github.com/guangyizhangbci/PLL-Emotion-EEG",
    keywords=[
        "artificial intelligence",
        "deep learning",
        "partial label learning",
        "eeg",
        "emotion recognition"
    ],
    install_requires=[
        "torch>=1.6",
        "numpy>=1.19.5",
        "matplotlib>=3.3.4",
        "tqdm>=4.62.3",
        "PyYAML>=6.0",
        "scipy>=1.5.4",
        "scikit-learn>=0.24.2"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
