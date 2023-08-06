from setuptools import setup, find_packages


setup(
    name="glassio",
    version="0.4.1",
    description="a micro webframework based on fastapi and motor",
    url="https://gitlab.com/viert/glassio",
    author="Pavel Vorobyev",
    author_email="aquavitale@yandex.ru",
    license="MIT",
    packages=[pkg for pkg in find_packages() if pkg.startswith("glassio")],
    include_package_data=True,
    package_data={"glassio": ["*.txt", "*.py", "*.tmpl"]},
    python_requires=">=3.11",
    install_requires=[
        "fastapi[all]",
        "uvicorn",
        "pymongo",
        "motor",
        "pydantic",
        "ipython",
        "requests",
        "bcrypt",
    ],
    entry_points={"console_scripts": ["glassio=glassio.command:main",]},
)
