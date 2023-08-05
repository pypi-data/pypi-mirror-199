from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'kabbes_pypi_builder': 
        [ 
            'Templates/default/{-{src_name}-}/{-{package_name}-}/__init__.py',
            'Templates/default/{-{src_name}-}/{-{package_name}-}/__main__.py',
            'Templates/default/{-{src_name}-}/{-{package_name}-}/CONFIG.json',
            'Templates/default/LICENSE', 
            'Templates/default/MANIFEST.in',
            'Templates/default/pyproject.toml', 
            'Templates/default/requirements.txt',
            'Templates/default/setup.cfg',
            'Templates/default/setup.py',
            'CONFIG.json'
        ]
        }
    )

