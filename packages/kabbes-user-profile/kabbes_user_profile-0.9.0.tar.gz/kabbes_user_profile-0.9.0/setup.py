from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'user_profile': 
        [ 
            'CONFIG.json',
            'Templates/default.json'
        ]
        }
    )