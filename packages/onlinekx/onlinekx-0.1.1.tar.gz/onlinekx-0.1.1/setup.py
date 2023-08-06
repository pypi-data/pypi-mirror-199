from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='onlinekx',
      version='0.1.1',
      description='The onlinekx joke in the world',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='onlinekx joke comedy flying circus',
      url='http://github.com/storborg/onlinekx',
      author='Ben',
      author_email='onlinekx@example.com',
      license='MIT',
      packages=['onlinekx'],
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['onlinekx-joke=onlinekx.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
