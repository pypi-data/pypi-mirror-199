from distutils.core import setup
setup(
  name = 'spamBot101',
  packages = ['spamBot101'],
  version = '0.1',
  license='MIT',
  description = 'A simple spam bot for WhatsApp. It can spam a message a given number of times or spam forever. It can be stopped by pressing ctrl.',
  author = 'Sushil Dhakal',
  author_email = 'sushilldhakal25@gmail.com',
  url = 'https://github.com/sushil3125/Spam-Bot-using-Python',
  download_url = 'https://github.com/sushil3125/Spam-Bot-using-Python/blob/main/projectSpamBot.exe',
  install_requires=[
          'pyautogui'
      ],
  classifiers=[ 
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)