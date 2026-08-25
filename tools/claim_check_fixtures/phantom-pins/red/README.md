# phantom-pins red fixture

Exactly one line here is a phantom pin. scikit-learn is not in requirements.txt:

    scikit-learn==1.7.1

Everything below must NOT fire, or the check is too loose to trust.

numpy is a real dependency, so pinning it is honest:

    numpy==2.5.1

python_dotenv is written with an underscore, which PyPI treats as the same name
as the python-dotenv in requirements.txt:

    python_dotenv==1.2.2

Prose may name a library the project does not install. scikit-learn is built on
numpy, and saying so is a fact about scikit-learn, not a dependency claim.
