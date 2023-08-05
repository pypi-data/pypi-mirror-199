from setuptools import setup, find_packages


setup_args = dict(
    name='SeleCrawler',
    version='0.0.1',
    description='Collection Of Tools To Ease Selenium Operation',
    packages=find_packages(),
    author='Gee Tech Labs',
    author_email='geetechlabs@gmail.com',
    keywords=['Selenium', 'Crawler', 'Browser', 'BrowserAutomation']
)

install_requires = [
    'webdriver-manager==3.8.5',
    'selenium==4.8.2',
    'undetected-chromedriver==3.4.6'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
