import random

SUBJ_INFINITIVE = 0
SUBJ_1PS = 0
SUBJ_2PS = 1
SUBJ_3PS = 2
SUBJ_1PP = 3
SUBJ_2PP = 4
SUBJ_3PP = 5

STANDARD_SUBJECTS = [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP]

class Quiz(object):
    def __init__(self, conjugator, allowable_verbs, tenses):
        self._conjugator = conjugator
        self._allowable_tenses = tenses
        self._allowable_verbs = allowable_verbs

    def get_question(self):
        verb = random.choice(self._allowable_verbs)
        tense = random.choice(self._allowable_tenses)
        return (verb, tense)

    def check_answers(self, verb, tense, answers):
        subjects = STANDARD_SUBJECTS
        assert(len(answers) == len(subjects))

        return [answer in self._conjugator.conjugate(verb, tense, subject) for (answer, subject) in zip(answers, subjects)]