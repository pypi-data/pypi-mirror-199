# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser ="""
# Author:KuoYuan Li  
ex1:
'''python
import colabcam  
colabcam.take_photo(filename)  
'''  
"""
setup(
        name='colabcam',   
        version='1.0.0',   
        description='take picture from cam in colab',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/colabcam',      
        packages=['colabcam'],   
        include_package_data=True,
        keywords = ['colab', 'webcam','take_photo','take_img','record_video_timed'],   # Keywords that define your package best
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
      ],
)
