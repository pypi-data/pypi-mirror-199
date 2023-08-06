import re
from typing import List

organic_subset = ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'I']
organic_aromatic = ['b', 'c', 'n', 'o', 'p', 's']
bonds = ['.', '-', '=', '#', '$', ':', '/', '\\']
branch = ['(', ')']
ring_re = re.compile(r'^\d{1,}$')


def split_smiles(smiles_str: str) -> List[str]:
    """ split_smiles: splits a simple molecular-input line-entry system
    (SMILES) string into individual characters. Individual characters include:

     - Organic atoms ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I']
     - Organic aromatic atoms ['b', 'c', 'n', 'o', 'p', 's']
     - Bonds ['.', '-', '=', '#', '$', ':', '/', '\\']
     - Branches ['(', ')']
     - Inorganic atoms (i.e., "[Au]" is considered a unique element)

    Rings indications (integer characters) are appended to the previous SMILES
    character.

    Args:
        smiles_str (str): SMILES string to split element-wise

    Returns:
        List[str]: list of SMILES elements ordered as they appear in the input
            SMILES string
    """

    elements = []
    _smi_chars = list(smiles_str)
    _tmp = ''
    _inorg = False
    for idx, c in enumerate(_smi_chars):
        if (c in organic_subset or c in organic_aromatic
           or c in bonds or c in branch) and not _inorg:
            elements.append(c)
            continue
        elif c == '[':
            _inorg = True
            _tmp += c
            continue
        elif c == ']':
            _inorg = False
            _tmp += c
            elements.append(_tmp)
            _tmp = ''
            continue
        elif _inorg:
            _tmp += c
            continue
        elif ring_re.match(c):
            elements[-1] += c
            continue
        elif c == '%' and ring_re.match(_smi_chars[idx + 1]):
            elements[-1] += c
            continue
        elif c == 'r' and elements[-1] == 'B':  # Bromine
            elements[-1] += c
            continue
        elif c == 'l' and elements[-1] == 'C':  # Chlorine
            elements[-1] += c
            continue
        else:
            raise RuntimeError(
                f'Unexpected SMILES character: {c}, {smiles_str}'
            )
    if _inorg:
        raise RuntimeError(f'Unclosed inorganic atom detected: {smiles_str}')
    return elements


class SmilesEncoder:

    def __init__(self, smiles_strings: List[str]) -> None:
        """ SmilesEncoder: one-hot encoding for simple molecular-input line-
        entry system (SMILES) strings. Supplied SMILES strings are used to
        construct a dictionary of one-hot vectors, each representing a unique
        SMILES element.

        Args:
            smiles_strings (List[str]): list of SMILES strings to construct
                dictionary with

        Returns:
            None
        """

        _unique_elements = []
        for s in smiles_strings:
            _elements = split_smiles(s)
            for e in _elements:
                if e in _unique_elements:
                    continue
                _unique_elements.append(e)
        self.element_dict = {}
        _n_elem = len(_unique_elements)
        for idx, e in enumerate(_unique_elements):
            _val = [0] * _n_elem
            _val[idx] = 1
            self.element_dict[e] = _val

    def encode(self, smiles_str: str) -> List[List[int]]:
        """ SmilesEncoder.encode: encodes a simple molecular-input line-entry
        system (SMILES) string into a 2D list, size [n_elements,
        n_dictionary_elements] (List of lists, each sublist comprised of one-
        hot encoding)

        Args:
            smiles_str (str): SMILES string to encode

        Returns:
            List[List[int]]: encoded SMILES string, shape (n_elements,
                n_dictionary_elements)
        """

        _elements = split_smiles(smiles_str)
        vectors = []
        for e in _elements:
            if e not in list(self.element_dict.keys()):
                raise RuntimeError(f'Unexpected SMILES character: {e}')
            vectors.append(self.element_dict[e])
        return vectors

    def encode_many(self, smiles_strings: List[str]) -> List[List[List[int]]]:
        """ SmilesEncoder.encode_many: encodes multiple smiles string using
        SmilesEncoder.encode().

        Args:
            smiles_strings (List[str]): list of SMILES strings to encode

        Returns:
            List[List[List[int]]]: encoded smiles strings, shape [n_strings,
                n_elements, n_dictionary_elements]
        """

        return [self.encode(s) for s in smiles_strings]

    def decode(self, encoded_smiles: List[List[int]]) -> str:
        """ SmilesEncoder.decode: decode a SMILES string currently
        represented as a list of one-hot vectors. Input should be of shape
        (n_elements, n_dictionary_elements).

        Args:
            encoded_smiles (List[List[str]]): encoded SMILES string shape
                (n_elements, n_dictionary_elements)

        Returns:
            str: decoded SMILES string
        """

        smiles_string = ''
        for v in encoded_smiles:
            _found = False
            for e in list(self.element_dict.keys()):
                if v == self.element_dict[e]:
                    _found = True
                    smiles_string += e
                    break
            if not _found:
                raise RuntimeError(f'Unexpected character vector: {v}')
        return smiles_string

    def decode_many(self, encoded_smiles: List[List[List[int]]]) -> List[str]:
        """ SmilesEncoder.decode_many: decode multiple SMILES strings
        currently represented as lists of one-hot vectors. Input should be of
        shape (n_strings, n_elements, n_dictionary_elements).

        Args:
            encoded_smiles (List[List[List[int]]]): SMILES strings in one-hot
                vector form; shape (n_strings, n_elements,
                n_dictionary_elements)

        Returns:
            List[str]: decoded SMILES strings
        """

        return [self.decode(e) for e in encoded_smiles]
