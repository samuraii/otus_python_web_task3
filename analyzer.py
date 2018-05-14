import ast
import argparse
import os
import collections
import nltk
import git
import shutil


def make_list_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file_handler:
        return file_handler.read()


def get_file_names(path_to_dir):
    filenames = []
    for dirname, dirs, files in os.walk(path_to_dir, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
    return filenames


def get_syntax_trees_from_files(file_names):
    trees = []

    for filename in file_names:
        file_content = get_file_content(filename)

        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            continue

        trees.append(tree)

    return trees


def get_all_functions_from_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def remove_special_names(function_names_list):
    return [name for name in function_names_list if not (name.startswith('__') and name.endswith('__'))]


def is_verb(word):
    if not word:
        return False
    pos_info = nltk.pos_tag([word])
    return pos_info[0][1] == 'VB'


def verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_function_names(trees):
    name_lists = [get_all_functions_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_all_verbs(function_names_list):
    verb_lists = [verbs_from_function_name(function_name) for function_name in function_names_list]
    return make_list_flat(verb_lists)


def clone_repo_to_tmp_folder(repo_url):
    DIR_NAME = "tmp"
    if os.path.isdir(DIR_NAME):
        shutil.rmtree(DIR_NAME)
    os.mkdir(DIR_NAME)
    repo = git.Repo.init(DIR_NAME)
    origin = repo.create_remote('origin', repo_url)
    origin.fetch()
    origin.pull(origin.refs[0].remote_head)


def print_top_ten_words(words):
    print('total %s words, %s unique' % (len(words), len(set(words))))
    print('-' * 20)
    for word, occurrence in collections.Counter(words).most_common(10):
        print(word, occurrence)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='The source should be a path to folder, or a github repo url.')
    parser.add_argument('-rep', '--repo', help='If this is true, the repo will be used.', type=bool, default=False)
    args = parser.parse_args()

    if args.repo:
        print('The following repo will be analyzed: {}'.format(args.source))
        clone_repo_to_tmp_folder(args.source)
        path = os.path.join('tmp')
    else:
        path = os.path.join(args.source)

    file_names = get_file_names(path)
    files_syntax_trees = get_syntax_trees_from_files(file_names)
    function_names = get_all_function_names(files_syntax_trees)
    verbs = get_all_verbs(function_names)
    print_top_ten_words(verbs)
    shutil.rmtree('tmp', ignore_errors=True)


if __name__ == '__main__':
    main()
