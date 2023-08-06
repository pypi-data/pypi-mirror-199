from distutils.core import setup
setup(
  name = 'aib_logging',         # How you named your package folder (MyLib)
  packages = ['aib_logging'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'add custom logs for AIB pipeline',   # Give a short description about your library
  author = 'Akib Shaikh',                   # Type in your name
  author_email = 'shaikhakib.k@gmail.com',      # Type in your E-Mail
  url = 'https://github.vodafone.com/akib-shaikh',   # Provide either the link to your github or to your website
  download_url = 'https://github.vodafone.com/akib-shaikh/aib_logging/archive/refs/tags/v0.2.tar.gz',    # I explain this later on
  install_requires=[            # I get to this in a second
          "google-cloud-logging",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)
