from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'kabbes_repository_generator': 
            [ 
                'Templates/default/.gitignore',
                'Templates/default/README.md', 
                'CONFIG.json'
            ]
            }
    )