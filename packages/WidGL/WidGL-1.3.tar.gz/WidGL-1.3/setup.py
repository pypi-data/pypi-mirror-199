from setuptools import setup
requirements = ["keyboard",
                "pygame_widgets", "colorama", "numpy", "colored","mouse"]
setup(name='WidGL',
      version='1.3',
      description='small and compact widgets distributions',
      packages=['WidGL'],
      author_email='pvana621@gmail.com',
      install_requires=requirements,
      zip_safe=False)
