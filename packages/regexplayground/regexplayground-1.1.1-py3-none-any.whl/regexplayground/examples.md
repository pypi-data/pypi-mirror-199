Examples for Python regular expressions are shown below. You can modify such code snippets and pressing the **Enter** key will update the corresponding output.

As a good practice, always use **raw strings** to construct the pattern, unless other formats are required. This will avoid conflict between special meaning of the backslash character in regular expressions and string literals.

### Examples for `re.search()`

```python
sentence = 'This is a sample string'
# check if 'sentence' contains the pattern described by RE argument
bool(re.search(r'is', sentence))

# ignore case while searching for a match
bool(re.search(r'this', sentence, flags=re.I))

# example when pattern isn't found in the input string
bool(re.search(r'xyz', sentence))

# use raw byte strings for patterns if input is of byte data type
bool(re.search(rb'is', b'This is a sample string'))
```

### String and Line anchors

```python
# match the start of the input string
bool(re.search(r'\Ahi', 'hi hello\ntop spot'))

# match the start of a line
bool(re.search(r'^top', 'hi hello\ntop spot', flags=re.M))

# match the end of strings
words = ['surrender', 'up', 'newer', 'do', 'era', 'eel', 'pest']
[w for w in words if re.search(r'er\Z', w)]

# check if there's a whole line 'par'
bool(re.search(r'^par$', 'spare\npar\ndare', flags=re.M))
```

### Examples for `re.findall()`

```python
# match 'par' with optional 's' at start and optional 'e' at end
re.findall(r'\bs?pare?\b', 'par spar apparent spare part pare')

# numbers >= 100 with optional leading zeros
# Python 3.11 supports possessive quantifiers
# re.findall(r'\b0*+\d{3,}\b', '0501 035 154 12 26 98234')
re.findall(r'\b0*[1-9]\d{2,}\b', '0501 035 154 12 26 98234')

# if multiple capturing groups are used, each element of output
# will be a tuple of strings of all the capture groups
re.findall(r'([^/]+)/([^/,]+),?', '2020/04,1986/Mar')

# normal capture group will hinder ability to get the whole match
# non-capturing group to the rescue
re.findall(r'\b\w*(?:st|in)\b', 'cost akin more east run against')

# useful for debugging purposes as well
re.findall(r':.*?:', 'green:3.14:teal::brown:oh!:blue')
```

### Examples for `re.split()`

```python
# split based on one or more digit characters
re.split(r'\d+', 'Sample123string42with777numbers')

# split based on digit or whitespace characters
re.split(r'[\d\s]+', '**1\f2\n3star\t7 77\r**')

# to include the matching delimiter strings as well in the output
re.split(r'(\d+)', 'Sample123string42with777numbers')

# multiple capture groups example
# note that the portion matched by b+ isn't present in the output
re.split(r'(a+)b+(c+)', '3.14aabccc42')

# use non-capturing group if capturing is not needed
re.split(r'hand(?:y|ful)', '123handed42handy777handful500')
```

### Backreferencing within the search pattern

```python
# whole words that have at least one consecutive repeated character
words = ['effort', 'flee', 'facade', 'oddball', 'rat', 'tool']
[w for w in words if re.search(r'\b\w*(\w)\1\w*\b', w)]
```

### Working with matched portions

```python
# re.Match object
re.search(r'so+n', 'too soon a song snatch')

# retrieving entire matched portion, note the use of [0]
motivation = 'Doing is often better than thinking of doing.'
re.search(r'of.*ink', motivation)[0]

# capture group example
purchase = 'coffee:100g tea:250g sugar:75g chocolate:50g'
m = re.search(r':(.*?)g.*?:(.*?)g.*?chocolate:(.*?)g', purchase)
# to get the matched portion of the second capture group
m[2]

# to get a tuple of all the capture groups
m.groups()
```

### Examples for `re.finditer()`

```python
# numbers < 350
m_iter = re.finditer(r'\d+', '45 349 651 593 4 204 350')
[m[0] for m in m_iter if int(m[0]) < 350]

# start and end+1 index of each matching portion
m_iter = re.finditer(r'so+n', 'song too soon snatch')
[m.span() for m in m_iter]
```

### Examples for `re.sub()`

```python
# add something to the start of every line
ip_lines = "catapults\nconcatenate\ncat"
re.sub(r'^', r'* ', ip_lines, flags=re.M).splitlines(True)

# replace 'par' only at the start of a word
re.sub(r'\bpar', r'X', 'par spar apparent spare part')

# same as: r'part|parrot|parent'
re.sub(r'par(en|ro)?t', r'X', 'par part parrot parent')

# remove the first two columns where : is delimiter
re.sub(r'\A([^:]+:){2}', '', 'apple:123:banana:cherry')
```

### Backreferencing in the replacement section

```python
# remove any number of consecutive duplicate words separated by space
# use \W+ instead of space to cover cases like 'a;a<-;a'
re.sub(r'\b(\w+)( \1)+\b', r'\1', 'aa a a a 42 f_1 f_1 f_13.14')

# add something around the matched strings
re.sub(r'\d+', r'(\g<0>0)', '52 apples and 31 mangoes')

# swap words that are separated by a comma
re.sub(r'(\w+),(\w+)', r'\2,\1', 'good,bad 42,24')

# example with both capturing and non-capturing groups
re.sub(r'(\d+)(?:abc)+(\d+)', r'\2:\1', '1000abcabc42 12abcd21')
```

### Using functions in the replacement section of `re.sub()`

```python
# factorial is imported from the math module
numbers = '1 2 3 4 5'
def fact_num(m): return str(factorial(int(m[0])))
re.sub(r'\d+', fact_num, numbers)

# using lambda
re.sub(r'\d+', lambda m: str(factorial(int(m[0]))), numbers)
```

### Examples for lookarounds

```python
# change 'cat' only if it is not followed by a digit character
# note that the end of string satisfies the given assertion
# 'catcat' has two matches as the assertion doesn't consume characters
re.sub(r'cat(?!\d)', 'dog', 'hey cats! cat42 cat_5 catcat')

# change whole word only if it is not preceded by : or -
re.sub(r'(?<![:-])\b\w+\b', r'X', ':cart <apple -rest ;tea')

# extract digits only if it is preceded by - and followed by ; or :
re.findall(r'(?<=-)\d+(?=[:;])', '42 apple-5, fig3; x-83, y-20: f12')

# words containing 'b' and 'e' and 't' in any order
words = ['sequoia', 'questionable', 'exhibit', 'equation']
[w for w in words if re.search(r'(?=.*b)(?=.*e).*t', w)]

# match if 'do' is not there between 'at' and 'par'
bool(re.search(r'at((?!do).)*par', 'fox,cat,dog,parrot'))

# match if 'go' is not there between 'at' and 'par'
bool(re.search(r'at((?!go).)*par', 'fox,cat,dog,parrot'))
```

### Examples for `re.compile()`

Regular expressions can be compiled using the `re.compile()` function, which gives back a `re.Pattern` object. The top level `re` module functions are all available as methods for this object. Compiling a regular expression helps if the RE has to be used in multiple places or called upon multiple times inside a loop (speed benefit). By default, Python maintains a small list of recently used RE, so the speed benefit doesn't apply for trivial use cases.

```python
pet = re.compile(r'dog')
type(pet)

bool(pet.search('They bought a dog'))

bool(pet.search('A cat crossed their path'))

pat = re.compile(r'\([^)]*\)')
pat.sub('', 'a+b(addition) - foo() + c%d(#modulo)')

pat.sub('', 'Hi there(greeting). Nice day(a(b)')
```

