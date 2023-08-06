import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faker_to_kafka",
    version="0.0.1",
    author="dormi330",
    author_email="dormi330@gmail.com",
    description="produce fake data to kafka",
    long_description="produce fake data to kafka, support csv and json",
    long_description_content_type="text/markdown",
    url="https://github.com/zqWu/faker-to-kafka",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "Faker==17.0.0",
        "kafka-python==2.0.2",
        "PyYAML==6.0"
    ],
)
