# coding:utf-8

from setuptools import setup, Extension
# or
# from distutils.core import setup
with open('README.md',encoding='utf-8') as f:
    long_description = f.read()
 
setup(
        name='colabcam',   
        version='1.0.2',   
        description='Process image from webcam in colab',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/colabcam',      
        packages=['colabcam'],   
        include_package_data=True,
        keywords = ['colab', 'webcam','javascript','take_photo','take_img','record_video_timed'],   # Keywords that define your package best
        install_requires=['mediapipe',],
        classifiers=['License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',]
)
