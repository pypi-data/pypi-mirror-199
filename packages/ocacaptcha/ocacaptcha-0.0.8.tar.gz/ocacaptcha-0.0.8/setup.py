from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ocacaptcha',
  version='0.0.8',
  description='Solving captcha hcaptcha, recaptcha, funcaptcha, TikTok captcha)',
  url='',  
  author='Nazarii',
  author_email='nazar.muxaulyk961@mail.ru',
  license='MIT', 
  classifiers=classifiers,
  keywords='tiktokcaptcha, hcaptcha, recaptcha, funcaptcha', 
  packages=find_packages(),
  install_requires=['base64', 'urllib.request', 'requests' , 'hashlib', 'random', 'time', 'selenium'] 
)