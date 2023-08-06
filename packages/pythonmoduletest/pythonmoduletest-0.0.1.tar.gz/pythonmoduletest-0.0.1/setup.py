from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'python package install test'
LONG_DESCRIPTION = 'add subtract multiply divide'

# 配置
setup(
       # 名称必须匹配文件名 'pythonmoduletest'
        name="pythonmoduletest", 
        version=VERSION,
        author="CremiyGu",
        author_email="shanghainewyork@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # 需要和你的包一起安装，例如：'caer'
        
        keywords=['python', 'install test'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X ",
            "Operating System :: Microsoft :: Windows",
        ]
)