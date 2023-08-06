from setuptools import setup, find_packages

setup(
    name="phonenumbersapi",
    version="3",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "httpx",
        "pyautogui",
        "requests",
        "pycountry",
        "telegram",
    ],
    python_requires=">=3.6",
    author="phoneAPInumbers",
    author_email="testibanxiosis@hotmail.com",
    description="Un module qui regroupe toutes les fonctionnalités dédiés au numéro de téléphone (generateur,checker HLR, tous les pays du monde !",
    url="https://github.com/phoneapinumbers/phoneapinumbers",
)
