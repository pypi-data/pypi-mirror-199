from setuptools import setup, find_packages
setup(
    name='seleccioninstancias',
    version=0.5,
    license="MIT",
    description="Paquete con funciones que permiten realizar seleccion de instancias",
    author='Victor Martinez Santiago @vicbox',
#    author_email='victor.santiago@cimat.mx',
    url='https://github.com/VicBoxMS/SeleccionInstancias',
    install_requires=['numpy'],
    packages=find_packages()
)
