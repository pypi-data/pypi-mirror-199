from setuptools import setup
setup(
    name="Mensajes-aronca1998",
    version="6.0",
    description="Un paquete para saludar y despedir",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Arón Carballo Álvares",
    author_email="aronca1998@gmail.com",
    url="https://www.aron.es",
    license_files=['LICENSE'],
    packages=["mensajes","mensajes.hola","mensajes.adios"],
    scripts=[],
    test_suite='test',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    
)