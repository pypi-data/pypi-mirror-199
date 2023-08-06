import sys
import re

print("Code is running...")

def get_path():
    frame = sys._getframe()
    while frame.f_back:
        frame = frame.f_back

        if frame.f_globals.get('__name__') == '__main__':
            return frame.f_globals['__file__']
        
    return None

def transpile(code):
    code = re.sub(r'(?<!\')(?:=>)(?!\')', ':', code)

    code = re.sub(r'([a-zA-Z_]\w*):([^:\n]+)', r'\1(\2)', code)

    # Later, perhaps.
    # code = re.sub(r'(?<!["\'])\b(def|function)\b(?![\'"\w])', lambda match: "function" if match.group(1) == "def" else "def", code)

    return code

def run(exit=0):
    path = get_path()

    with open(path, "r") as file:
        try:
            code = file.read()

        except FileNotFoundError:
            raise FileNotFoundError("File: '"+path+"' could not be found.")

        try:
            match = re.search(r"""(?:[^"\']|^)import\s+arrowpython(?:[^"\']|$)""", code)
            code = code[match.end():].strip()

        except AttributeError:
            raise SyntaxError('Could not find import statement. Try putting "import arrowpython" on the first line.')

        code = transpile(code)
        print(code)

    exec(code)

    raise SystemExit(exit)

run()