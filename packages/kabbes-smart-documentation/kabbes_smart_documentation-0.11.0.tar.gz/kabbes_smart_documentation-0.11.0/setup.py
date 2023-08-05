from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'kabbes_smart_documentation': 
        [ 
            'Templates/default/.github/workflows/*.yml',
            'Templates/sphinx/conf.py',
            'Templates/sphinx/index.rst',
            'Templates/sphinx/make.bat',
            'Templates/sphinx/Makefile',
            'CONFIG.json',
            'sphinx_script.sh'
        ]
        }
    )