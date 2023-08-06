from typing import Union, List


def revac(b: bytes, root=True) -> Union[List[int], bytes]:
    """
    Another very basic symmetric cipher function that just makes sure keys don't get stored in cleartext

    :param b: (bytes) byte sequence to cipher
    :param root: (bool) used for recursion, do not give any arguments
    :return: (bytes) ciphered byte sequence
    """
    l = len(b)
    hl = int(l / 2)
    if l == 1:
        return b
    if not l % 2 and l <= 2:
        result = [b[1], b[0]]
    elif not l % 3 and l <= 3:
        result = [b[2], b[1], b[0]]
    elif not l % 4:
        result = revac(b[0:hl], root=False) + revac(b[hl:l], root=False)
    elif not l % 6:
        result = revac(b[0:hl], root=False) + revac(b[hl:l], root=False)
    else:
        result = revac(b[0:hl], root=False) + [b[hl]] + revac(b[hl + 1 : l], root=False)
    if root:
        # function is recursive and works with List[int] in internal calls, but will need to output bytes at the end
        return bytes(result)
    return result
