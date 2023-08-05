# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @author :yinzhengjie
# blog:https://www.cnblogs.com/yinzhengjie

from setuptools import setup, find_packages, Extension

setup(
    # 指定项目名称，我们在后期打包时，这就是打包的包名称，当然打包时的名称可能还会包含下面的版本号哟~
    name='airpage',
    # 指定版本号
    version='0.1.3',
    # 这是对当前项目的一个描述
    description='based on airtest',
    # 作者是谁，指的是此项目开发的人，这里就写你自己的名字即可
    author='eaglebaby',
    # 作者的邮箱
    author_email='2229066748@qq.com',
    # 写上项目的地址，比如你开源的地址开源写博客地址，也开源写GitHub地址，自定义的官网地址等等。
    url='https://gitee.com/eagle-s_baby/airpage',
    # 指定包名，即你需要打包的包名称，要实际在你本地存在哟，它会将指定包名下的所有"*.py"文件进行打包哟，但不会递归去拷贝所有的子包内容。
    # 综上所述，我们如果想要把一个包的所有"*.py"文件进行打包，应该在packages列表写下所有包的层级关系哟~这样就开源将指定包路径的所有".py"文件进行打包!
    platforms='Windows',
    packages=find_packages(),
    python_requires='==3.9.*',
    # 需要安装的依赖
    install_requires=[
        'py_trees',
        'airtest',
        'pyautogui',
        'files3',
        'pywin32',
        "pydotplus",
        'wxauto',  #
    ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'ap_new = airpage.cmd_entry:CMD_NewProject',
        'ap_version = airpage.cmd_entry:CMD_Version',
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)