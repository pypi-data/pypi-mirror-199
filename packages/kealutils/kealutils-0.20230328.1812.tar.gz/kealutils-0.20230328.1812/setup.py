import setuptools

setuptools.setup(
    name="kealutils",
    version="0.20230328.1812",
    author="realizer",
    author_email="bonfireof@gmail.com",
    description="Some utils for me.",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "kealutils"},
    # packages=setuptools.find_packages(where="kealutils"),
    package_dir={"kealutils": "kealutils",
                 "kealutils.test": "test" },
    packages=["kealutils", "kealutils.test"],
    python_requires=">=3.1",
    install_requires=[
    ]
)
