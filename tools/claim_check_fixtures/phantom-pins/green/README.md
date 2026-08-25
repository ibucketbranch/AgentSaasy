# phantom-pins green fixture

Every pin here names a package that is in requirements.txt:

    numpy==2.5.1
    PYTHON_DOTENV>=1.2.2

The name comparison is case-insensitive and treats "-" and "_" as the same
character, so the second line is the python-dotenv that requirements.txt pins.

Prose about scikit-learn appears here on purpose. It is not a dependency, and a
check that flagged the mention rather than a pin would fire on this fixture.
