from setuptools import setup

setup(
    name='sanews_aleph',
    entry_points={
        'aleph.crawlers': [
            'TheNewAge = sanews_aleph.crawlers:TheNewAgeCrawler',
        ]
    },
    version='0.0.1',
    description='Aleph crawler to index South African news',
    url='https://github.com/public-people',
    author='JD Bothma',
    author_email='jbothma@gmail.com',
    license='MIT',
    packages=["sanews_aleph"],
    zip_safe=False,
    install_requires=[
        'python-slugify',
    ],
    dependency_links=[
        'https://github.com/public-people/sanews/tarball/master#egg=sanews',
    ]
)
