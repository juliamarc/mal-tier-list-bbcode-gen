import setuptools


entry_points = {
    'console_scripts': [
        'mal-tier-list-bbcode-gen = mal_tier_list_bbcode_gen.cli:main',
    ]
}

setuptools.setup(
    name='mal-tier-list-bbcode-gen',
    version='0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='BBCode generator for MyAnimeList blog posts',
    url='https://github.com/juliamarc/mal-tier-list-bbcode-gen',
    # TODO look up in documentation
    install_requires=['click', 'bbcode', 'ezodf', 'lxml'],
    entry_points=entry_points,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
