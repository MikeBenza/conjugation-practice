from __future__ import print_function

import os.path
import pprint
import sys
import traceback
import time

import parser

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

class Conjugator(object):
    def __init__(self, directory, language):
        self._verbs = parser.load_verb_file(os.path.join(directory, 'verbs-' + language + '.xml'))
        self._conjugations = parser.load_conjugation_file(os.path.join(directory, 'conjugation-' + language + '.xml'))
        self._filters = {}

    def conjugate(self, verb, tense, subject):
        (template_name, aspirate_h) = self._verbs[verb]
        template = self._conjugations[template_name]
        inf_ending = template[TENSE_INFINITIVE][SUBJ_INFINITIVE][0]
        root = verb[::-1].replace(inf_ending[::-1], '', 1)[::-1] # Replace the infinitive ending only at the end of the string
        endings = template[tense][subject]
        return [root + ending for ending in endings]

    def filter_by_template(self, templates):
        tt = tuple(sorted(templates))
        if not self._filters.has_key(tt):
            r = []
            print("len: %d" % (len(templates)))
            for (verb, (template, aspirate_h)) in self._verbs.items():
                if template in templates:
                    r.append(verb)
            self._filters[tt] = r

        return self._filters[tt]
