from __future__ import print_function

import os

import conjugator
import quiz

PRONOUNS = ['je', 'tu', 'il', 'nous', 'vous', 'ils']

TENSE_INFINITIVE = 0
TENSE_IND_PRESENT = 1
TENSE_IND_IMPERFECT = 2
TENSE_IND_FUTURE = 3
TENSE_IND_SIMPLE_PAST = 4
TENSE_CON_PRESENT = 5
TENSE_SUB_PRESENT = 6
TENSE_SUB_IMPERFECT = 7
TENSE_IMP_PRESENT = 8
TENSE_PAR_PRESENT = 9
TENSE_PAR_PAST = 10

SUBJ_INFINITIVE = 0
SUBJ_1PS = 0
SUBJ_2PS = 1
SUBJ_3PS = 2
SUBJ_1PP = 3
SUBJ_2PP = 4
SUBJ_3PP = 5

STANDARD_SUBJECTS = [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP]

SUBJ_MS = 0
SUBJ_MP = 1
SUBJ_FS = 2
SUBJ_FP = 3

def run_quiz(conjugator, quiz):
    stop = False
    while not stop:
        (verb, tense) = quiz.get_question()
        answers = []
        print(u"Verb: %s" % (verb))
        for pronoun in PRONOUNS:
            text = u"%s + %s: " % (pronoun, verb)
            print(text, end="")
            answers.append(raw_input())
        print(quiz.check_answers(verb, tense, answers))


if __name__ == '__main__':
    conjugator = conjugator.Conjugator(os.path.join('verbiste-0.1.41', 'data'), 'fr')
    quiz = quiz.Quiz(conjugator, conjugator.filter_by_template(['aim:er', 'fin:ir', 'man:ger']), [TENSE_IND_PRESENT])
    run_quiz(conjugator, quiz)