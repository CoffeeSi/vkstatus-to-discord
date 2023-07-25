from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read()

setup(
    name="vk-discord",
    version="1.0",
    description="VK status translator to Discord status",
    package_dir={"":"vk-discord"},
    packages=find_packages(where="vk-discord"),
    long_description=long_description,
    url="https://github.com/CoffeeSi/vkstatus-to-discord",
    author="CoffeeSi",
    author_email="ewgenik02032006@gmail.com",
    license="MIT",
    classifiers=[
        "LICENSE :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11.4",
        "Operating System :: Windows"
    ],
    install_requires=requirements,
    python_requires=">=3.10",
)
