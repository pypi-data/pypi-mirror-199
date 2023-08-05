from setuptools import setup
requirements = ["Pygame==2.1.1", "keyboard",
                "pygame_widgets", "colorama", "numpy", "colored","mouse"]
setup(name='WidGL',
      version='1.0',
      description='small and compact widgets distributions',
      packages=['WidGL'],
      author_email='pvana621@gmail.com',
      install_requires=requirements,
      zip_safe=False)
