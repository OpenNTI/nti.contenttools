import codecs
from setuptools import setup, find_packages

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
        'nti_html_latex_parser = nti.contenttools.parser.html_to_tex:main',
        'nti_mathcounts_html_latex_parser = nti.contenttools.parse_mathcounts_html_latex:main',
        'nti_csv_latex_concepts = nti.contenttools.script.csv_latex_concepts_tree:main'
    ]
}

TESTS_REQUIRE = [
    'nti.testing',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.contenttools',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI contentt tools",
    long_description=(_read('README.rst') + '\n\n' + _read("CHANGES.rst")),
    license='Apache',
    keywords='Base',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/NextThought/nti.contenttools",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'lxml',
        'nti.contentfragments',
	'nti.property',
        'nti.schema',
        'Pillow',
        'simplejson',
        'six',
        'z3c.baseregistry',
        'zope.component',
        'zope.exceptions',
        'zope.interface',
        'zope.location',
        'zope.security',
        'zope.traversing',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    entry_points=entry_points
)
