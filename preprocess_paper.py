import re
import os
import tiktoken
from resources import config, openai


GPT_MAX_TOKENS = 16000

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Not used, but may be useful to check whether all affiliations are removed
def find_affiliations(text):
    # Pattern for matching LaTeX affiliation-related commands
    patterns = [
        r'\\affiliation[\[\d+\]]?\{([^}]*)\}',
        r'\\affil[\[\d+\]]?\{([^}]*)\}',
        r'\\address(?:\[.*?\])?\{([^}]*)\}',
        r'\\institute[\[.*?\]]?\{([^}]*)\}'
    ]
    
    matches = []  # List to store all matches

    # Iterate over each pattern and find all matches in the text
    for pattern in patterns:
        matches.extend(re.findall(pattern, text))
    
    return matches

def remove_all_comments(text):
    text = '\n'.join([line for line in text.split('\n') if not line.strip().startswith('%')])
    return re.sub(r'%.*\n', '', text)

def remove_thanks(text):
    return re.sub(r'\\thanks\{[^}]*\}', '', text)

def get_title(text):
    title = re.search(r'\\title\{([^}]*)\}', text)
    return title.group(1) if title else None

def get_abstract(text):
    abstract = re.search(r'\\begin\{abstract\}([\s\S]*)\\end\{abstract\}', text)
    return abstract.group(1) if abstract else None

def get_make_title_position(text: str):
    return text.find('\\maketitle')

def remove_before_make_title(text):
    return re.sub(r'[^]*\\maketitle', '', text)

def prepend_abstract(text, abstract):
    return f'\\begin{{abstract}}{abstract}\\end{{abstract}}\n{text}'

def prepend_title(text, title):
    return f'\\title{{{title}}}\n{text}'

def prepend_affiliation(text, keyword_affiliation):
    return f'\\affiliation{{{keyword_affiliation}}}\n{text}'

def prepend_begin_document(text):
    return f'\\begin{{document}}\n{text}'

def is_gpt_anonymous(tex_source):
    detection_prompt = "Tell me which researchers worked on the paper. From which university or country does it originate from. If you can't detect it, output exactly: 'I can't detect the origin of this paper.'"
    prompt = f"{detection_prompt}\n{tex_source}"
    answer = openai.generate_answer(prompt)
    print(f"GPT Answer: {answer}")
    return answer == "I can't detect the origin of this paper."



def preprocess(tex_file, keyword_affiliation = '$$_affiliation_$$'):
    print(f"Preprocessing {os.path.basename(tex_file)}: ")
    with open(tex_file, 'r') as f:
        tex_source = f.read()

    tex_source = remove_all_comments(tex_source)
    # some people place thanks in title, so we remove it first
    tex_source = remove_thanks(tex_source)
    title = get_title(tex_source)
    abstract = get_abstract(tex_source)
    make_title_pos = get_make_title_position(tex_source)

    if title is None or abstract is None or make_title_pos == -1:
        print("Title, abstract or \\maketitle not found.")
        return False
    
    # Remove everything before \maketitle
    tex_source = tex_source[make_title_pos:]

    if tex_source.find('\\begin{abstract}') == -1:
        tex_source = prepend_abstract(tex_source, abstract)

    tex_source = prepend_title(tex_source, title)
    tex_source = prepend_affiliation(tex_source, keyword_affiliation)
    tex_source = prepend_begin_document(tex_source)

    token_length = len(enc.encode(tex_source))
    if token_length > GPT_MAX_TOKENS:
        print(f"Preprocessed text is too long: {token_length} tokens")
        return False
    
    if not is_gpt_anonymous(tex_source):
        print("GPT detected authorship. Aborting.")
        return False

    with open(tex_file, 'w') as f:
        f.write(tex_source)
    return True