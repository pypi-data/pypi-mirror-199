## Project description

### Tetun Tokenizer

Tetun tokenizer is a Python package for tokenizing a string (or a text) into tokens using:
1. Word, punctuations, or special characters delimiters `TetunStandardTokenizer()`.
2. Whitespace delimiter `TetunWhiteSpaceTokenizer()`.
3. Blank lines as a delimiter `TetunBlankLineTokenizer()`.

Additionally, it is also allowed us to tokenize a string (or a text) by:
1. Strings and numbers and ignore punctuations and special characters `TetunSimpleTokenizer()`.
2. Strings only and ignore numbers, punctuations, and special characters `TetunWordTokenizer()`.

### Installation

To install Tetun tokenizer, run the following command:

```
python3 -m pip install tetun-tokenizer
```

or simply use:

```
pip install tetun-tokenizer
```

### Usage

To use the Tetun tokenizer, from the `tetuntokenizer` package, import a specific tokenizer class and the tokenize function as follows:

1. Using  `TetunStandardTokenizer()` to tokenize a string.

```python
from tetuntokenizer import TetunStandardTokenizer

tokenizer = TetunStandardTokenizer()

string_text = "Ha'u, Gabriel de Jesus, ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tokenizer.tokenize(string_text)
print(output)
```

The output will be:

```
["Ha'u", ',', 'Gabriel', 'de', 'Jesus', ',', 'ita-nia', 'maluk', "di'ak", '.', "Ha'u", 'iha', '$', '0.25', 'atu', 'fó', 'ba', 'ita', '.']
```

2. Using `TetunWhiteSpaceTokenizer()` to tokenize a string.

```python
from tetuntokenizer import TetunWhiteSpaceTokenizer

tokenizer = TetunWhiteSpaceTokenizer()

string_text = "Ha'u, Gabriel de Jesus, ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tokenizer.tokenize(string_text)
print(output)
```

The output will be:

```
["Ha'u,", 'Gabriel', 'de', 'Jesus,', 'ita-nia', 'maluk', "di'ak.", "Ha'u", 'iha', '$0.25', 'atu', 'fó', 'ba', 'ita.']
```

3. Using `TetunBlankLineTokenizer()` to tokenize a string.

```python
from tetuntokenizer import TetunBlankLineTokenizer

tokenizer = TetunBlankLineTokenizer()

string = """
        Ha'u, Gabriel de Jesus, ita-nia maluk di'ak.
        Ha'u iha $0.25 atu fó ba ita.
        """
output = tokenizer.tokenize(string_text)
print(output)
```

The output will be:

```
["\n            Ha'u, Gabriel de Jesus, ita-nia maluk di'ak.\n            Ha'u iha $0.25 atu fó ba ita.\n            "]
```

4. Using `TetunSimpleTokenizer()` to tokenize a string.

```python
from tetuntokenizer import TetunSimpleTokenizer

tokenizer = TetunSimpleTokenizer()

string_text = "Ha'u, Gabriel de Jesus, ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tokenizer.tokenize(string_text)
print(output)
```

The output will be:

```
["Ha'u", 'Gabriel', 'de', 'Jesus', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', '0.25', 'atu', 'fó', 'ba', 'ita']
```

5. Using `TetunWordTokenizer()` to tokenize a string.

```python
from tetuntokenizer import TetunWordTokenizer

tokenizer = TetunWordTokenizer()

string_text = "Ha'u, Gabriel de Jesus, ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tokenizer.tokenize(string_text)
print(output)
```

The output will be:

```
["Ha'u", 'Gabriel', 'de', 'Jesus', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', 'atu', 'fó', 'ba', 'ita']
```

To print the resulting string to the console, with each element on a new line, you can use `for` loop or simply use `join` as follows:

```
print('\n'.join(output))
```

The output will be:

```
Ha'u
Gabriel
de
Jesus
ita-nia
maluk
di'ak
Ha'u
iha
atu
fó
ba
ita
```

You can also use the tokenizer to tokenize a text from a file. Here is an example:

```python
# Assume that we use Path instead of a string for the file path
from pathlib import Path
from tetuntokenizer import TetunSimpleTokenizer


file_path = Path("/myfile/example.txt")

try:
    with corpus_path.open('r', encoding='utf-8') as f:
    contents = [line.strip() for line in f]
except FileNotFoundError:
    print(f"File not found at: {corpus_path}")

output = '\n'.join(tokenizer.tokenize(str(contents)))
print(output)

```

There are a few more ways to read file contents that you can use to achieve the same output.