import cPickle
import os
import sys

from dtree_util import *


# - given a text file where each line is a question sentence, use the
#   stanford dependency parser to create a dependency parse tree for each sentence
def dparse(question_file, rawpath):
    out_file = open(raw_path, 'w')

    # change these paths to point to your stanford parser.
    # make sure to use the lexparser.sh file in this directory instead of the default!
    parser_out = os.popen(
        "/home/michael/Documents/tools/stanford-corenlp-full-2016-10-31/lexparser.sh " + question_file).readlines()
    for line in parser_out:
        out_file.write(line)

    out_file.close()


# - function that parses the resulting stanford parses
#   e.g., "nsubj(finalized-5, john-1)"
def split_relation(text):
    # print("split_relation - text", text)
    rel_split = text.split('(')
    rel = rel_split[0]
    deps = rel_split[1][:-1]
    if len(rel_split) != 2:
        # print 'error ', rel_split
        sys.exit(0)

    else:
        dep_split = deps.split(',')

        # more than one comma (e.g. 75,000-19)
        if len(dep_split) > 2:
            fixed = []
            half = ''
            for piece in dep_split:
                piece = piece.strip()
                if '-' not in piece:
                    half += piece

                else:
                    fixed.append(half + piece)
                    half = ''

            dep_split = fixed

        final_deps = []
        for dep in dep_split:
            words = dep.split('-')
            word = words[0]
            ind = int(words[len(words) - 1])

            if len(words) > 2:
                word = '-'.join([w for w in words[:-1]])

            final_deps.append((ind, word.strip()))

        return rel, final_deps


# - given a list of all the split relations in a particular sentence,
#   create a dtree object from that list
def make_tree(plist):
    # print "plist", plist
    # print "he", type(plist[0])
    # identify number of tokens
    max_ind = -1
    for rel, deps in plist:
        for ind, word in deps:
            if ind > max_ind:
                max_ind = ind

    # load words into nodes, then make a dependency tree
    nodes = [None for i in range(0, max_ind + 1)]
    for rel, deps in plist:
        for ind, word in deps:
            nodes[ind] = word
    # print "rel", rel
    # print "deps", deps
    tree = dtree(nodes)

    # add dependency edges between nodes
    for rel, deps in plist:
        par_ind, par_word = deps[0]
        kid_ind, kid_word = deps[1]
        tree.add_edge(par_ind, kid_ind, rel)

    return tree


def make_split(fold_file, qid_file, questions_file, answers_file):
    folds = open(fold_file, 'r')
    qids = open(qid_file, 'r')
    questions = open(questions_file, 'r')
    answers = open(answers_file, 'r')

    split_train = []
    split_test = []
    split_dev = []

    for fold in folds:
        fold = fold.strip()
        question = questions.readline().strip()
        answer = answers.readline().strip()
        qid = int(qids.readline())

        if fold == "train":
            split_train.append([[question], answer, qid])
        elif fold == "test":
            split_test.append([[question], answer, qid])
        elif fold == "dev":
            split_dev.append([[question], answer, qid])

    return split_train, split_test, split_dev


def make_splits(fold_file, qid_file, questions_file, answers_file):
    split_train, split_test, split_dev = make_split(fold_file, qid_file, questions_file, answers_file)
    splits = {'train': split_train, 'test': split_test, 'dev': split_dev}
    return splits


# - given all dependency parses of a dataset as well as that dataset (in the same order),
#   dumps a processed dataset that can be fed into QANTA:
#   (vocab, list of dep. relations, list of answers, and dict of {fold: list of dtrees})
def process_question_file(raw_parses, fold_file, qid_file, question_file, answer_file):
    parses = open(raw_parses, 'r')

    split = make_splits(fold_file, qid_file, question_file, answer_file)

    parse_text = []
    new = False
    cur_parse = []

    for line in parses:

        line = line.strip()

        if not line:
            new = True

        if new:
            parse_text.append(cur_parse)
            cur_parse = []
            new = False

        else:
            rel, final_deps = split_relation(line)
            cur_parse.append((rel, final_deps))

    print len(parse_text)


    # make mapping from answers: questions
    # and questions: [sentence trees]
    count = 0
    tree_dict = {}
    for key in split:
        hist = split[key]
        # print hist

        tree_dict[key] = []
        for text, ans, qid in hist:
            for i in range(0, len(text)):
                tree = make_tree(parse_text[count])
                tree.ans = ans.lower().replace(' ', '_').strip()
                tree.dist = i
                tree.qid = qid
                tree_dict[key].append(tree)
                count += 1

    vocab = []
    rel_list = []
    ans_list = []

    for key in tree_dict:
        qlist = tree_dict[key]
        for tree in qlist:
            if key == 'train':
                if tree.ans not in ans_list:
                    ans_list.append(tree.ans)

            if tree.ans not in vocab:
                vocab.append(tree.ans)

            tree.ans_ind = vocab.index(tree.ans)

            for node in tree.get_nodes():
                if node.word not in vocab:
                    vocab.append(node.word)

                node.ind = vocab.index(node.word)

                for ind, rel in node.kids:
                    if rel not in rel_list:
                        rel_list.append(rel)

    print 'rels: ', len(rel_list)
    print 'vocab: ', len(vocab)
    print 'ans: ', len(ans_list)

    cPickle.dump((vocab, rel_list, ans_list, tree_dict),
                 open('/home/michael/Documents/projects/qanta/data/final_hist_split', 'wb'))


if __name__ == '__main__':
    question_file = '/home/michael/Documents/projects/my_qanta/processed/history_questions'
    answer_file = '/home/michael/Documents/projects/my_qanta/processed/history_answers'
    qid_file = '/home/michael/Documents/projects/my_qanta/processed/history_qids'
    fold_file = '/home/michael/Documents/projects/my_qanta/processed/history_folds'
    raw_path = '/home/michael/Documents/projects/my_qanta/history_raw_parses'
    dparse(question_file, raw_path)
    process_question_file(raw_path, fold_file, qid_file, question_file, answer_file)
