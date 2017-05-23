import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

TESTS_REQUIRE = [
    'nti.testing',
    'zope.testrunner',
]

entry_points = {
    "z3c.autoinclude.plugin": [
        'target = nti.contenttools',
    ],
    'console_scripts': [
        'nti_import_docx = nti.contenttools.word2latex:main',
        'nti_import_epub = nti.contenttools.import_epub:main',
        'nti_glossary_finder = nti.contenttools.glossary_term_finder:main',
        'nti_glossary_exporter = nti.contenttools.glossary_json_exporter:main',
        'nti_import_cnx = nti.contenttools.import_cnx:main',
        'nti_epub_latex_parser = nti.contenttools.parser.epub_to_latex:main',
        'nti_html_latex_parser = nti.contenttools.parse_html_latex:main',
        'nti_mathcounts_html_latex_parser = nti.contenttools.parse_mathcounts_html_latex:main'
    ]
}

setup(
    name='nti.contenttools',
    version=VERSION,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Content Tools",
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    license='Proprietary',
    keywords='Content tools',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['nti'],
    install_requires=[
        'setuptools',
        'docutils',
        'lxml',
        'nti.contentfragments',
        'nti.schema',
        'Pillow',
        'simplejson',
        'six',
        'zope.component',
        'zope.exceptions',
        'zope.interface',
        'zope.location',
        'zope.security',
        'zope.traversing',
        'zopyx.txng3.ext',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points
)
