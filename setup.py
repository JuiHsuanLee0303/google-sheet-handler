from setuptools import setup, find_packages

setup(
    name="google-sheet-handler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client==2.108.0",
        "google-auth==2.23.4",
        "google-auth-oauthlib==1.1.0",
        "google-auth-httplib2==0.1.1",
        "pyyaml==6.0.1",
        "aiohttp==3.9.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "python-dotenv==1.0.0",
        ],
    },
    python_requires=">=3.7",
) 