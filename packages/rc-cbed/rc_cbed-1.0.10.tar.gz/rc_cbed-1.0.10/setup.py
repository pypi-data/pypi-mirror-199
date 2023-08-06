from setuptools import setup, find_packages

setup(
    name='rc_cbed',
    version='1.0.10',    
    description='rc_cbed network design to restore and center CBED images',
    url='https://github.com/Ivanlh20/rc_cbed',
    author='Ivan Lobato',
    author_email='ivanlh20@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    install_requires=['numpy', 'h5py', 'matplotlib'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
    include_package_data=True,
    package_data={'': ['test_data.h5']},
)