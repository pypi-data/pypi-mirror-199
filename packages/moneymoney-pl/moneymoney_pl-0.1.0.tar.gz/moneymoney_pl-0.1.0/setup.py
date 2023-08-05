from setuptools import setup, Command
import site
import os
import platform

class Procedure(Command):
    description = "Show release procedure"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("""Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Modificar el Changelog en README
  * python setup.py uninstall; python setup.py install
  * git commit -a -m 'moneymoney_pl-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * python setup.py sdist
  * twine upload dist/moneymoney_pl-{0}.tar.gz 
  * python setup.py uninstall
""".format(__version__))

#  * Crea un nuevo ebuild de moneymoney_pl Gentoo con la nueva versión
#  * Subelo al repositorio del portage

## Class to define doxygen command
class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"

    user_options = [
      # The format is (long option, short option, description).
      ( 'user=', None, 'Remote ssh user'),
      ( 'directory=', None, 'Remote ssh path'),
      ( 'port=', None, 'Remote ssh port'),
      ( 'server=', None, 'Remote ssh server'),
  ]

    def initialize_options(self):
        self.user="root"
        self.directory="/var/www/html/doxygen/moneymoney_pl/"
        self.port=22
        self.server="127.0.0.1"

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")      
        command=f"""rsync -avzP -e 'ssh -l {self.user} -p {self.port} ' html/ {self.server}:{self.directory} --delete-after"""
        print(command)
        os.system(command)
        os.chdir("..")
  
## Class to define uninstall command
class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/moneymoney_pl*".format(site.getsitepackages()[0]))
        else:
            os.system("pip uninstall moneymoney_pl")

########################################################################

## Version of moneymoney_pl captured from commons to avoid problems with package dependencies
__version__= None
with open('moneymoney_pl/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__VERSION__=")!=-1:
            __version__=line.split('"')[1]


setup(name='moneymoney_pl',
     version=__version__,
     description='Python module to read and write LibreOffice and MS Office files using uno API',
     long_description='Project web page is in https://github.com/turulomio/moneymoney_pl',
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='',
     url='https://github.com/turulomio/moneymoney_pl',
     author='turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['moneymoney_pl'],
     install_requires=[],
     cmdclass={'doxygen': Doxygen,
               'uninstall':Uninstall, 
               'procedure': Procedure,
              },
     zip_safe=False,
     test_suite = 'moneymoney_pl.tests',
     include_package_data=True
)
