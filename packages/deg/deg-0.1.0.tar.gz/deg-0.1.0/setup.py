from setuptools import setup, Extension, find_packages



with open('README.md') as f:
	extd_desc = f.read()

with open('LICENSE') as f:
    license = f.read()

requirements_noversion = [
	'networkx',
    'matplotlib'
]
setup(
	# Meta information
	name				= 'deg',
	version				= '0.1.0',
	author				= 'Supratik Chatterjee',
	author_email			= 'supratikdevm96@gmail.com',
	url				= 'https://github.com/supratikchatterjee16/deg',
	description			= 'A Graph library to manage inheritance rules',
	keywords			= ['graph', 'visualize', 'dependency', 'inheritance'],
	install_requires		= requirements_noversion,
	# build information
	py_modules			= ['deg'],
	packages			= find_packages(),
	package_dir			= {'deg' : 'deg'},
	include_package_data		= True,
	long_description		= extd_desc,
	long_description_content_type	='text/markdown',
	# package_data			= {'deg' : [
	# 					'databank/*',
	# 					'datadump/*',
	# 					'factuals/*'
	# 					]},

	zip_safe			= True,
	# https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py
	classifiers			= [
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	license 			= license
)