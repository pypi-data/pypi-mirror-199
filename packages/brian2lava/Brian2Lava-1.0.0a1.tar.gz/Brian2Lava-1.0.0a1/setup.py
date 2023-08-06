from setuptools import setup

setup(
	name='Brian2Lava',
	version='1.0.0a1',  # consider adding '__version__' to 'brian2lava.__init__.py', but requires unified management of versions
	author='Carlo Michaelis, Francesco Negri, Winfried Oed, Jannik Luboeinski, Andrew Lehr, Tristan Stöber',
	author_email='carlo.michaelis@gmail.com',
	packages=['brian2lava', 'brian2lava.device', 'brian2lava.codegen', 'brian2lava.writer'],
	python_requires='>3.8',
	url='https://gitlab.com/tetzlab/brian2lava',
	license='MIT',
	description='An open source Brian2 interface for the neuromorphic computing framework Lava',
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	package_data = {
		"brian2lava/codegen/templates": ["*.py_"],
		"brian2lava/templates": ["*.py.j2"]
	},
    include_package_data=True,
	install_requires=[
		"brian2>=2.5.1",
		"jinja2>=2.7",
		"numpy==1.23.5",
		"pytest",
		"scipy",
		"markupsafe==2.0.1",
		"lava-nc>=0.6.0",
		"matplotlib",
		"regex>=2022.10.31"
	],
)
