from setuptools import setup


setup(
    name='djangorestframework-simple-captcha',
    version='0.1a1',
    license='BSD',
    description='Captcha field for Django Rest framework serializers',
    author='Sergei Sinitsyn',
    author_email='sinitsinsv@gmail.com',
    packages=['rest_framework_captcha'],
    install_requires=['djangorestframework', 'django-simple-captcha'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
