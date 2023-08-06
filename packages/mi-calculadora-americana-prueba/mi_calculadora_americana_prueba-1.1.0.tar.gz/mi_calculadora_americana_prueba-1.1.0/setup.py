from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mi_calculadora_americana_prueba",
    version="1.1.0",
    author="Tu Nombre",
    author_email="tu_correo@ejemplo.com",
    description="Una simple calculadora de Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/mi-calculadora",
    packages=[""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "py-expression-eval"
    ],
    entry_points={
        'console_scripts': [
            'mi_calculadora = calculadora:main'
        ]
    },
)