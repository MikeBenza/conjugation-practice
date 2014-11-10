import conjugator

import traceback
import xml.dom.minidom

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

def _get_node_children(node):
    return (child for child in node.childNodes if child.nodeType == child.ELEMENT_NODE)

def _get_children_nodes(node, name):
    return (child for child in _get_node_children(node) if child.nodeName == name)

def _first_or_none(generator):
    try:
        return generator.next()
    except StopIteration:
        return None
    
def _get_child_node(node, name):
    return _first_or_none(_get_children_nodes(node, name))
    
def _get_node_text(node):
    try:
        return node.childNodes[0].data
    except IndexError:
        return u''
    
def _load_conjugation(template, mode, tense, subjects):
    result = {}
    conjugations = [node for node in _get_children_nodes(_get_child_node(_get_child_node(template, mode), tense), u'p')]
    
    for subject_id in range(len(subjects)):
        if conjugations[subject_id]:
            texts = [_get_node_text(x) for x in _get_children_nodes(conjugations[subject_id], u'i')]
            result[subjects[subject_id]] = [_get_node_text(x) for x in _get_children_nodes(conjugations[subject_id], u'i')]
        else:
            result[subjects[subject_id]] = []

    return result
    
def load_verb_file(path):
    verbs = {}
    doc = xml.dom.minidom.parse(path)
    root = _get_child_node(doc, u'verbs-fr')
    
    for verb in _get_children_nodes(root, u'v'):
        i = _get_node_text(_get_child_node(verb, u'i'))
        t = _get_node_text(_get_child_node(verb, u't'))
        h = _get_child_node(verb, u'aspirate-h') != None
        verbs[i] = (t, h)
    return verbs
            
def load_conjugation_file(path):
    conjugations = {}
    doc = xml.dom.minidom.parse(path)
    root = _get_child_node(doc, u'conjugation-fr')
    
    for template in _get_children_nodes(root, u'template'):
        template_name = None
        try:
            conjugation = {}
            template_name = _get_node_text(template.attributes['name'])

            conjugation[TENSE_INFINITIVE]        = _load_conjugation(template, u'infinitive',  u'infinitive-present', [SUBJ_INFINITIVE])
            conjugation[TENSE_IND_PRESENT]       = _load_conjugation(template, u'indicative',  u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_IND_IMPERFECT]     = _load_conjugation(template, u'indicative',  u'imperfect',          [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_IND_FUTURE]        = _load_conjugation(template, u'indicative',  u'future',             [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_IND_SIMPLE_PAST]   = _load_conjugation(template, u'indicative',  u'simple-past',        [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_CON_PRESENT]       = _load_conjugation(template, u'conditional', u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_SUB_PRESENT]       = _load_conjugation(template, u'subjunctive', u'present',            [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_SUB_IMPERFECT]     = _load_conjugation(template, u'subjunctive', u'imperfect',          [SUBJ_1PS, SUBJ_2PS, SUBJ_3PS, SUBJ_1PP, SUBJ_2PP, SUBJ_3PP])
            conjugation[TENSE_IMP_PRESENT]       = _load_conjugation(template, u'imperative',  u'imperative-present', [SUBJ_2PS, SUBJ_1PP, SUBJ_2PP])
            conjugation[TENSE_PAR_PRESENT]       = _load_conjugation(template, u'participle',  u'present-participle', [SUBJ_INFINITIVE])
            conjugation[TENSE_PAR_PAST]          = _load_conjugation(template, u'participle',  u'past-participle',    [SUBJ_MS, SUBJ_MP, SUBJ_FS, SUBJ_FP])
            
            conjugations[template_name] = conjugation
        except Exception, e:
            traceback.print_exc()
        
    return conjugations
