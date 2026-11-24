class SurveyProblem(Exception):
    def __init__(self, code, text, status=422):
        self.code, self.status = code, status
        super().__init__(text)
