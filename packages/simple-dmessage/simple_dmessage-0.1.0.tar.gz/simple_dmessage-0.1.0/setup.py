from setuptools import setup, find_packages

setup(
    name='simple_dmessage',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['discord.py'],
    entry_points={
        'console_scripts': [
            'send_direct_message=simple_dmessage.send_direct_message:main',
        ],
    },
    author='Lee Kin Emree',
    author_email='nspielman@live.com',
    description='A package for sending direct messages via Discord',
    url='https://github.com/nooooaaaaah/simple_discord_message',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
