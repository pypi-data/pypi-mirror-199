from setuptools import setup, find_packages

setup(
    name='auto-env-config',  # 包名
    version='v1.0.8',  # 版本
    description="Configuring your python environment automatically.",  # 包简介
    long_description=open('README.md', encoding='utf-8').read(),  # 读取文件中介绍包的详细内容
    long_description_content_type='text/markdown',
    include_package_data=True,  # 是否允许上传资源文件
    author='曾钦李',  # 作者
    author_email='1838696034@qq.com',  # 作者邮件
    maintainer='',  # 维护者
    maintainer_email='',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.7',  # 设置python版本要求
    install_requires=[''],  # 安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },  # 设置命令行工具(可不使用就可以注释掉)
)
