def title(msg: str, verbose: bool) -> None:
    if verbose: print('- {}'.format(msg))

def subtitle(msg: str, verbose: bool) -> None:
    if verbose: print('  > {}'.format(msg))