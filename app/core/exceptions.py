class PersonalAnalyzerException(Exception):
    pass


class AlembicException(PersonalAnalyzerException):
    """
    Migration failure.
    """
