from setuptools import find_packages, setup

setup(
    name="django-rtk-upfront",
    version="0.6.0",
    description="Extension of django-rtk that requires a password in the registration step",
    long_description="Extension of django-rtk that requires a password in the registration step",
    long_description_content_type="text/x-rst",
    url="https://github.com/mnieber/django-rtk-home/blob/main/django-rtk-upfront/README.md",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=["django-rtk"],
    zip_safe=False,
    python_requires=">=3.6",
)
