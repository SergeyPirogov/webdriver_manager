#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import setuptools

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='webdriver_manager',
    python_requires=">=3.7",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['webdriver_manager*']),
    include_package_data=True,
    version='3.9.0',
    description='Library provides the way to automatically manage drivers for different browsers',
    author='Sergey Pirogov',
    author_email='automationremarks@gmail.com',
    url='https://github.com/SergeyPirogov/webdriver_manager',
    keywords=['testing', 'selenium', 'driver', 'test automation'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: '
        'Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    install_requires=[
        'requests',
        'python-dotenv',
        'tqdm',
        'packaging'
    ],
    package_data={
        "webdriver_manager": ["py.typed"]
    },
)
