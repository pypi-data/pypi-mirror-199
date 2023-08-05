from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='PyAutoCoder',
    version='1',
    packages=['PyAutoCoder'],
    url='https://github.com/GlobalCreativeApkDev/INDONESIAN_PROGRAMMERS/tree/main/PyAutoCoder',
    license='MIT',
    author='GlobalCreativeApkDev',
    author_email='globalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the automatic Python code generator "PyAutoCoder".',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "PyAutoCoder=PyAutoCoder.PyAutoCoder:main",
        ]
    }
)