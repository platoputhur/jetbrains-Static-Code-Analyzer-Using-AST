# write your code here
import re
import argparse
import os
import ast


class StyleChecker:
    def __init__(self, filepath):
        self.filepath = filepath
        self.line = None
        self.index = 0
        self.continuous_blank_line_counter = 0

    def analyse_line(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            asd: str
            for index, line in enumerate(lines, start=1):
                self.line = line
                self.index = index
                self.s001_check()
                self.s002_check()
                self.s003_check()
                self.s004_check()
                self.s005_check()
                self.s006_check()
                self.s007_check()
                self.s008_check()
                self.s009_check()
        self.s010_check()
        self.s011_check()
        self.s012_check()

    def s001_check(self):
        if len(self.line) > 79:
            print(f"{self.filepath}: Line {self.index}: S001 Too long")

    def s002_check(self):
        indentation_regex = re.compile(r'([\s]*).+')
        indentation_match = indentation_regex.search(self.line)
        if indentation_match:
            indentation_group = indentation_match.group(1)
            if len(indentation_group) % 4 != 0:
                print(f"{self.filepath}: Line {self.index}: S002 Indentation is not a multiple of four")

    def s003_check(self):
        # Checks if the line is a comment ie starting with a #
        # If so, this check is unnecessary
        comment_regex = re.compile(r'^\s*[#].*')
        if not comment_regex.search(self.line):
            # check if # exists in the line
            # If so split the line using #
            # And get the first item from the list.
            # Strip it from all the white spaces
            # Check if the last item is ;
            if '#' in self.line:
                line_split = self.line.split("#")
                line_without_comments: str = line_split[0]
                line_without_whitespaces = line_without_comments.strip()
            else:
                line_without_whitespaces = self.line.strip()
            if line_without_whitespaces:
                if line_without_whitespaces[-1] == ";":
                    print(f"{self.filepath}: Line {self.index}: S003 Unnecessary semicolon")

    def s004_check(self):
        if '#' in self.line:
            space_before_comment_regex = re.compile(r'.+?(\s*?)[#].*?$')
            spaces_match = space_before_comment_regex.search(self.line)
            if spaces_match:
                spaces = spaces_match.group(1)
                if len(spaces) < 2:
                    print(
                        f"{self.filepath}: Line {self.index}: S004 At least two spaces required before inline comments")

    def s005_check(self):
        todo_regex = re.compile(r'[#].*TODO.*', re.IGNORECASE)
        if todo_regex.search(self.line):
            print(f"{self.filepath}: Line {self.index}: S005 TODO found")

    def s006_check(self):
        empty_line_regex = re.compile(r'^\W+$')
        if empty_line_regex.match(self.line):
            self.continuous_blank_line_counter += 1
        else:
            if self.continuous_blank_line_counter > 2:
                print(f"{self.filepath}: Line {self.index}: S006 More than two blank lines used before this line")
                self.continuous_blank_line_counter = 0
            else:
                self.continuous_blank_line_counter = 0

    def s007_check(self):
        space_between_definition = re.compile(r'(class|def)(\s+)\w*')
        spaces_match = space_between_definition.search(self.line)
        if spaces_match:
            construction_name = spaces_match.group(1)
            spaces = spaces_match.group(2)
            if len(spaces) > 1:
                print(f"{self.filepath}: Line {self.index}: S007 Too many spaces after '{construction_name}'")

    def s008_check(self):
        class_style_check = re.compile(r'class(\s+)(\w*):')
        style_match = class_style_check.search(self.line)
        if style_match:
            class_name = style_match.group(2)
            if class_name[0].islower() or "_" in class_name:
                print(
                    f"{self.filepath}: Line {self.index}: S008 Class name {class_name} should be written in CamelCase")

    def s009_check(self):
        def_style_check = re.compile(r'def(\s+)([\w]*)\([\w]*?\):')
        style_match = def_style_check.search(self.line)
        if style_match:
            function_name = style_match.group(2)
            if function_name[0].isupper() or any(alphabet.isupper() for alphabet in function_name):
                print(
                    f"{self.filepath}: Line {self.index}: S009 Function name {function_name} should be written in "
                    f"snake_case")

    def s010_check(self):
        with open(self.filepath, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for item in node.args.args:
                        if any(alphabet.isupper() for alphabet in item.arg):
                            print(f"{self.filepath}: Line {node.lineno}: S010 Argument name {item.arg} should be "
                                  f"written in snake_case")

    def s011_check(self):
        with open(self.filepath, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        if any(alphabet.isupper() for alphabet in node.id):
                            print(f"{self.filepath}: Line {node.lineno}: S011 Variable {node.id} should be written in "
                                  f"snake_case")

    def s012_check(self):
        error_messages = []
        with open(self.filepath, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    line = node.lineno
                    args = node.args
                    if args is not None:
                        if args.defaults is not None:
                            for item in args.defaults:
                                if item is not None:
                                    if isinstance(item, ast.List):
                                        error_messages.append(f"{self.filepath}: Line {line}: "
                                                              f"S012 The default argument value is mutable")
        for item in set(error_messages):
            print(item)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_check')
    args = parser.parse_args()
    path_to_check = args.path_to_check
    files_list = []
    if os.path.exists(path_to_check):
        if os.path.isfile(path_to_check):
            file_name_to_check = os.path.basename(path_to_check)
            if file_name_to_check.split(".")[-1] == "py":
                style_checker = StyleChecker(path_to_check)
                style_checker.analyse_line()
                exit()
        elif os.path.isdir(path_to_check):
            for dir_path, _, files in os.walk(path_to_check):
                for file_name in files:
                    if file_name.split(".")[-1] == "py":
                        files_list.append(os.path.join(dir_path, file_name))

    files_list = sorted(files_list, key=lambda x: os.path.basename(x))
    for item in files_list:
        style_checker = StyleChecker(item)
        style_checker.analyse_line()


if __name__ == "__main__":
    main()
