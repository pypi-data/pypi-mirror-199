import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-fastly-tls-domain",
    "version": "1.1.0.a7",
    "description": "Manage the activation of a Tls Domain",
    "license": "Apache-2.0",
    "url": "https://github.com/aws-ia/cloudformation-fastly-resource-providers",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_fastly_tls_domain",
        "cdk_cloudformation_fastly_tls_domain._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_fastly_tls_domain._jsii": [
            "fastly-tls-domain@1.1.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_fastly_tls_domain": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.70.0, <3.0.0",
        "constructs>=10.1.292, <11.0.0",
        "jsii>=1.79.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
