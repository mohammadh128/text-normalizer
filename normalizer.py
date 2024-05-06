import re
import string
from regexes.currency import CURRENCY_REGEX
from regexes.email import EMAIL_REGEX
from regexes.quote import DOUBLE_QUOTE_REGEX, SINGLE_QUOTE_REGEX
from regexes.url import URL_REGEX
from pylatexenc.latex2text import LatexNodes2Text
import dictionary

def multiple_replace(text, chars_to_mapping):
    """
    replacing multiple characters at once as afunction
    args:
        text(str): input text.
        chars_to_mapping(dict): a dictionary. keys in this dictionaries replaced by their values.
    """
    pattern = "|".join(map(re.escape, chars_to_mapping.keys()))
    return re.sub(pattern, lambda m: chars_to_mapping[m.group()], str(text))


def fix_spaces(text):
    """
    Ffixing spaces including spaces around punctuations and and chars like ()[]{}
    also fixing space around period like '. ' we don't have issue for sent_tokenizing
    args:
        text: input text
    """
    text = " ".join(text.split())
    # remove space in []
    text = re.sub('\[\s*(.*?)\s*\]', r'[\1]', text)
    # remove spaces in ()
    text = re.sub('\(\s*(.*?)\s*\)', r'(\1)', text)
    #ADDS SPACE AFTER DOT(period) EXCEPT IF THE DOT IS DECIMAL POINT. SO IT DOESNT EFFECT DOTS IN NUMBERS.
    text = re.sub("""((?<=[A-Za-z0-9])\.(?=[A-Za-z]{2})|(?<=[A-Za-z]{2})\.(?=[A-Za-z0-9]))""", '. ', text)
    # Add space after comma(,) semicolons(;) colons(:) exclamation points(!) question marks(?)
    text = re.sub(r'(?<=[,:;!?])(?=[^\s])', r' ', text)
    # strip space befor punc but not after t
    text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)

    return text

def handle_latext(txt):
    """
    transform raw Latext text to human readable text
    args:
        txt: input text
    """
    return LatexNodes2Text().latex_to_text(txt)

def normalize(text):
    """
    main function"""

    text = text.replace("\n", " ").replace("\t", " ").replace("\\", "")
    text = re.sub(r'<.*?>', "", text) ## clean html tags
    text = text.replace('ـ', '')
    text = re.sub(f"([{string.punctuation}])\\1+", "\\1", text) # remove repetetive punctuations
    text = fix_spaces(text)
    if len(dictionary.abbreviations) > 0:
        text = multiple_replace(text, dictionary.abbreviations)

    if len(dictionary.titles) > 0:
        text = multiple_replace(text, dictionary.titles)

    text = handle_latext(text)
    if len(dictionary.currencies) > 0:
        text = multiple_replace(text, dictionary.currencies)






    text = SINGLE_QUOTE_REGEX.sub("'", text)
    text = DOUBLE_QUOTE_REGEX.sub('"', text)
    # text = CURRENCY_REGEX.sub(r" ", text)
    # text = URL_REGEX.sub(" ", text)
    # text = EMAIL_REGEX.sub(" ", text)

    return text


if __name__ == '__main__':
    import textwrap


    input_text = """
    [[[    we study             ]]]    {{{the structure of th}}}e  . ((( mather and aubry sets))) for the family of lagrangians given
    by the kinetic energy associated to a riemannian metric $ g$ on a closed manifold $ m$.
    in this case the (  euler-lagrange  ) flow is the {    geodesic  } flow of $(m,g)$. we prove that there exists a
    residual subset $ \mathcal g$ of the set of all conformal metrics to $g$, such that,
    if $ \overline g \in \mathcal g$ then the corresponding geodesic flow has a
    finitely many ergodic c-minimizing measures, for each non-trivial cohomology
    class $ c \in h^1(m,\mathbb{r})$. this implies that, for any $ c \in h^1(m,\mathbb{r})$,
    the quotient aubry set for the cohomology class c has a finite number of elements for
    this particular family of lagrangian systems.???!!!!
    `aa` Dr.Strangelove     Mrs.          aaaa $ 2฿
    """
    input_text = normalize(input_text)
    print(textwrap.fill(input_text))
