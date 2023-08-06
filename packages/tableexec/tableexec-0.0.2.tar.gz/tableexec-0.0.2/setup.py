from distutils.core import setup
setup(
  name = 'tableexec',
  packages = ["tableexec"],
  version = '0.0.2',
  description = 'Execute command for every row in Excel/ODS table.',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/tableexec',
  download_url = 'https://github.com/fantastic001/tableexec/tarball/0.0.1',
  keywords = ["excel", "spreadsheet"], 
  package_dir = {'tableexec': 'tableexec/'},
  classifiers = [],
  entry_points = {
    "console_scripts": [
      "tableexec = tableexec.__main__:main"
    ]
  },
  install_requires=[
    "pandas", 
    "odfpy",
    "xlrd"
  ] # dependencies listed here 
)
