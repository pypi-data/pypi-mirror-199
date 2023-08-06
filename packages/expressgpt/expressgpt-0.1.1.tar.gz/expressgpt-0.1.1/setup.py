from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="expressgpt",
    version="0.1.1",
    description="Run chatGPT anywhere",
    author="Digant Patel",
    author_email="pateldigant95@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "pynput",
        "pyautogui",
        "openai",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "expressgpt=expressgpt.expressgpt:main",
        ],
    },
)
