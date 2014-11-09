from __future__ import print_function

import xml.dom.minidom

import pprint
import random
import sys
import traceback
import time

CONJ_INFINITIVE = 0
CONJ_IND_PRESENT = 1
CONJ_IND_IMPERFECT = 2
CONJ_IND_FUTURE = 3
CONJ_IND_SIMPLE_PAST = 4
CONJ_CON_PRESENT = 5
CONJ_SUB_PRESENT = 6
CONJ_SUB_IMPERFECT = 7
CONJ_IMP_PRESENT = 8
CONJ_PAR_PRESENT = 9
CONJ_PAR_PAST = 10

SUBJ_INFINITIVE = 0
SUBJ_1PS = 0
SUBJ_2PS = 1
SUBJ_3PS = 2
SUBJ_1PP = 3
SUBJ_2PP = 4
SUBJ_3PP = 5

SUBJ_MS = 0
SUBJ_MP = 1
SUBJ_FS = 2
SUBJ_FP = 3

STANDARD_SUBJECTS = [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP]
PRONOUNS = {SUBJ_1PS: u'je', SUBJ_2PS: u'tu', SUBJ_3PS: u'il', SUBJ_1PP: u'nous', SUBJ_2PP: u'vous', SUBJ_3PP: u'ils'}
    

def get_node_children(node):
    return (child for child in node.childNodes if child.nodeType == child.ELEMENT_NODE)

def get_children_nodes(node, name):
    return (child for child in get_node_children(node) if child.nodeName == name)

def first_or_none(generator):
    try:
        return generator.next()
    except StopIteration:
        return None
    
def get_child_node(node, name):
    return first_or_none(get_children_nodes(node, name))
    
def get_node_text(node):
    try:
        return node.childNodes[0].data
    except IndexError:
        return u''
    
def get_conjugation(template, mode, tense, subjects):
    result = {}
    conjugations = [node for node in get_children_nodes(get_child_node(get_child_node(template, mode), tense), u'p')]
    
    for subject_id in range(len(subjects)):
        if conjugations[subject_id]:
            texts = [get_node_text(x) for x in get_children_nodes(conjugations[subject_id], u'i')]
            result[subjects[subject_id]] = [get_node_text(x) for x in get_children_nodes(conjugations[subject_id], u'i')]
        else:
            result[subjects[subject_id]] = []

    return result
    
def load_verb_file(path):
    verbs = {}
    doc = xml.dom.minidom.parse(path)
    root = get_child_node(doc, u'verbs-fr')
    
    for verb in get_children_nodes(root, u'v'):
        i = get_node_text(get_child_node(verb, u'i'))
        t = get_node_text(get_child_node(verb, u't'))
        h = get_child_node(verb, u'aspirate-h') != None
        verbs[i] = (t, h)
    return verbs
            
def load_conjugation_file(path):
    conjugations = {}
    doc = xml.dom.minidom.parse(path)
    root = get_child_node(doc, u'conjugation-fr')
    
    for template in get_children_nodes(root, u'template'):
        template_name = None
        try:
            conjugation = {}
            template_name = get_node_text(template.attributes['name'])

            conjugation[CONJ_INFINITIVE]        = get_conjugation(template, u'infinitive',  u'infinitive-present', [SUBJ_INFINITIVE])
            conjugation[CONJ_IND_PRESENT]       = get_conjugation(template, u'indicative',  u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_IND_IMPERFECT]     = get_conjugation(template, u'indicative',  u'imperfect',          [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_IND_FUTURE]        = get_conjugation(template, u'indicative',  u'future',             [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_IND_SIMPLE_PAST]   = get_conjugation(template, u'indicative',  u'simple-past',        [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_CON_PRESENT]       = get_conjugation(template, u'conditional', u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_SUB_PRESENT]       = get_conjugation(template, u'subjunctive', u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_SUB_IMPERFECT]     = get_conjugation(template, u'subjunctive', u'imperfect',          [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[CONJ_IMP_PRESENT]       = get_conjugation(template, u'imperative',  u'imperative-present', [SUBJ_2PS, SUBJ_1PP, SUBJ_2PP])
            conjugation[CONJ_PAR_PRESENT]       = get_conjugation(template, u'participle',  u'present-participle', [SUBJ_INFINITIVE])
            conjugation[CONJ_PAR_PAST]          = get_conjugation(template, u'participle',  u'past-participle',    [SUBJ_MS, SUBJ_MP, SUBJ_FS, SUBJ_FP])
            
            conjugations[template_name] = conjugation
        except Exception, e:
            if template_name:
                print("Failed to parse template %s: %s" % (template_name, e), file=sys.stderr)
                traceback.print_exc()
                sys.exit(1)
            else:
                print("Failed to parse template after %d previous templates: %s" % (len(conjugations.keys()), e), file=sys.stderr)
        
    return conjugations
    
def categorize(verbs):
    result = {}
    for (verb, (template, aspirate_h)) in verbs.items():
        if not result.has_key(template):
            result[template] = []
        result[template].append(verb)
    return result
    
def conjugate_verb(verb, conjugation, tense, subject):
    inf_ending = conjugation[CONJ_INFINITIVE][SUBJ_INFINITIVE][0]
    root = verb[::-1].replace(inf_ending[::-1], '', 1)[::-1]
    return root + conjugation[tense][subject][0]

def conjugate(verb, verbs, conjugations, tense, subject):
    (template, aspirate_h) = verbs[verb]
    conjugation = conjugations[template]
    return conjugate_verb(verb, conjugation, tense, subject)
    
if __name__ == '__main__':
    start = time.time()
    verbs = load_verb_file(r'verbiste-0.1.41\data\verbs-fr.xml')
    end = time.time()
    print("Loaded verbs in %.3f seconds" % (end - start))
    
    start = time.time()
    conjugations = load_conjugation_file(r'verbiste-0.1.41\data\conjugation-fr.xml')
    end = time.time()
    print("Loaded conjugations in %.3f seconds" % (end - start))
    
    cats = categorize(verbs)
    verb = random.choice(cats['aim:er'])
    
    for subject in STANDARD_SUBJECTS:
        print("%s + %s: %s" % (PRONOUNS[subject], verb, conjugate(verb, verbs, conjugations, CONJ_IND_PRESENT, subject)))
    