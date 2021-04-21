import setuptools


entry_points = {
    'console_scripts': [
        'mal-fav-bbcode-gen = mal_fav_bbcode_gen.cli:main',
    ]
}

setuptools.setup(
    name='mal-fav-bbcode-gen',
    version='0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='BBCode generator for MyAnimeList blog post',
    url='https://github.com/juliamarc/mal-fav-bbcode-gen',
    # TODO look up in documentation
    install_requires=['click', 'bbcode', 'ezodf', 'lxml'],
    entry_points=entry_points,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
