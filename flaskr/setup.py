from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask','flask_jsglue','flask_wtf','pymysql', 'wtforms_jsonschema2', 'json2html', 'pymongo', 'dnspython'
    ],
)
