from setuptools import setup, find_packages

setup(
    name="B0tHe1Per_test_api",
    version="0.1",
    author="Serj",
    author_email="buda_serj@yahoo.com",
    description="Test API for Bot Helper project",
    url='https://github.com/serjbuda/B0tHe1Per.git',
    packages=find_packages(),
    install_requires=['tkinter',
                      'subprocess',
                      'datatime',
                      're',
                      'shutil',
                      'string',
                      'unicodedata',
                      'collections'],
    entry_points={
        'console_scripts': [
            'bot_helper = B0tHe1Per_test_api.bot_interface:main'
        ]
    }
)
