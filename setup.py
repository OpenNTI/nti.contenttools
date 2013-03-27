#!/usr/bin/env python
from setuptools import setup, find_packages

entry_points = {
	'console_scripts': [
		'import_docx = nti.contenttools.word2latex:main',
	]
}

setup(
	name = 'nti.contenttools',
	version = '0.0',
	keywords = 'web',
	author = 'NTI',
	author_email = 'sean.jones@nextthought.com',
	description = 'NextThought Platform Content Development Tools',
	long_description = 'Dataserver README',
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers :: Education",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.7",
		"Framework :: Pylons :: ZODB :: Pyramid",
		"Internet :: WWW/HTTP",
		"Natural Language :: English",
		"Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
		],
        requires = [ 'nti.dataserver' ],
	packages = find_packages( 'src' ),
	package_dir = {'': 'src'},
	include_package_data = True,
	namespace_packages=['nti',],
	zip_safe = False,
	entry_points = entry_points
	)
