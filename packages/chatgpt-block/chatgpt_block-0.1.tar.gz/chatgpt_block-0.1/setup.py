from setuptools import setup, find_packages

setup(
    name='chatgpt_block',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai>=0.27.2',
        'requests>=2.28.2',
        'tiktoken>=0.3.2'
    ],
)

