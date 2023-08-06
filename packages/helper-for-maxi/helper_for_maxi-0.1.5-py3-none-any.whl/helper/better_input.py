from .better_print import better_print as BetterPrint


def better_input(text: str = None, end: str = None, delay: float = None):
    r"""Gets an input

    Prints the given text letter by letter using the specified delay and gets an input() after

    Parameters
    ----------
    text: Optional[str]
        The text that is printed letter by letter
        DEFAULT: None
    
    end: Optional[str]
        The text that is passed into the input() statement. 
        Be aware that this part is not printed letter by letter.
        DEFAULT: None

    delay: Optional[float]
        Changes the time between each printed letter
        DEFAULT: .01
    """
    
    if text is not None:
        BetterPrint(text, delay, False)
    if end is not None:
        res = input(end)
    else:
        res = input()
    return res