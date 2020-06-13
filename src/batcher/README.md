The following python tools must be installed using """pip install""" -> pip-tools

## Compilation
New logical dependencies must first be added to """requirement.in""".

To compile the required dependencies, the following command must be ran in terminal

pip-compile requirements.in > requirements.txt
pip install -r requirements.txt
