# representation.py

import string
from typing import Optional, Iterable

__all__ = [
    "remove_suffix",
    "remove_prefix",
    "indent",
    "group_sentences"
]

def group_sentences(sentences: Iterable[str]) -> str:
    """
    Groups seperated sentences into one string.

    :param sentences: The sentences to group.

    :return: The string of all the sentences.
    """

    return " ".join(
        [
            (
                value if any(
                    [
                        value.endswith(end)
                        for end in ('.', '!', '?', ':')
                    ]
                ) else value + "."
            )
            for value in sentences
        ]
    )
# end group_sentences

def remove_suffix(source: str, *, suffix: Optional[str] = " ") -> str:
    """
    Removes the suffix from the end of the string for the amount of positions.

    :param source: The source string.
    :param suffix: The part to remove.

    :return: The modified string.
    """

    if suffix is None:
        suffix = " "

    elif not suffix:
        return source
    # end if

    if suffix and source.endswith(suffix):
        i = 0

        for i, letter in enumerate(source[::-1]):
            if letter != suffix:
                break
            # end if
        # end for

        if i == 0:
            i = -1
        # end if

        return source[:-len(suffix) * i]
    # end if

    return source
# end remove_suffix

def remove_prefix(source: str, *, prefix: Optional[str] = " ") -> str:
    """
    Removes the suffix from the beginning of the string for the amount of positions.

    :param source: The source string.
    :param prefix: The part to remove.

    :return: The modified string.
    """

    if prefix is None:
        prefix = " "

    elif not prefix:
        return source
    # end if

    if prefix and source.startswith(prefix):
        i = 0

        for i, letter in enumerate(source):
            if letter != prefix:
                break
            # end if
        # end for

        if i == 0:
            i = 1
        # end if

        return source[len(prefix) * i:]
    # end if

    return source
# end remove_prefix

def indent(source: str, *, indentation: Optional[int] = 4) -> str:
    """
    Indents a string of object structures.

    :param indentation: The amount of spaces to indent according to.
    :param source: The source string.

    :return: The indented model structure.
    """

    if indentation is None:
        indentation = 4

    elif not indentation:
        return source
    # end if

    openers = "{[("
    closers = "}])"

    output = ""

    indents = 0
    new_line = False

    reindent = ""
    brackets = openers + closers

    for first in openers:
        for second in openers:
            source = source.replace(f"{first}{second}", f"{first} {second}")
        # end for
    # end for

    for char in source:
        for opener in openers:
            if char == opener:
                output += (
                    ("" if ((reindent in brackets) and (reindent != "")) else "\n") +
                    (" " * indents) + char
                ) + "\n"

                indents += indentation
                new_line = True

                break
            # end if
        # end for

        for closer in closers:
            if char == closer:
                indents -= indentation
                output += (
                    ("" if ((reindent in brackets) and (reindent != "")) else "\n") +
                    (" " * indents) + char
                ) + "\n"

                new_line = True

                break
            # end if
        # end for

        if (char not in brackets) and new_line:
            output += (" " * indents) + char
            new_line = False

        elif char not in brackets:
            output += char
        # end if

        reindent = char
    # end for

    lines = output.split("\n")

    new_lines = []

    for line in lines:
        try:
            if (new_line := remove_prefix(line))[0] in openers:
                new_lines[-1] += new_line

                continue
            # end if

        except IndexError:
            pass
        # end try

        new_lines.append(line)
    # end for

    output = "\n".join(new_lines)

    lines = output.split("\n")
    new_lines = []

    for line in lines:
        line = line.replace(", ", ",\n" + ("\t" * line.count('    ')))

        new_lines.append(line)
    # end for

    output = "\n".join(new_lines)

    lines = output.split("\n")
    new_lines = []

    for line in lines:
        try:
            if (new_line := remove_prefix(line)) == ",":
                new_lines[-1] += new_line

                continue
            # end if

        except IndexError:
            pass
        # end try

        new_lines.append(line)
    # end for

    output = "\n".join(new_lines)

    lines = output.split("\n")
    new_lines = []

    for line in lines:
        try:
            if (
                (
                    (new_line := remove_prefix(line)) in
                    ",".join(list(closers)) + ","
                ) and
                (new_lines[-1][-1] in openers)
            ):
                new_lines[-1] += new_line

                continue
            # end if

        except IndexError:
            pass
        # end try

        new_lines.append(line)
    # end for

    output = "\n".join(new_lines)

    lines = output.split("\n")
    new_lines = []
    excluded = []

    for i, line in enumerate(lines[:-1]):
        if i in excluded:
            continue
        # end if

        stripped_end_line = remove_prefix(
            lines[i + 1], prefix="\t"
        )
        stripped_end_line = remove_prefix(
            stripped_end_line
        )

        if (
            stripped_end_line.split() and
            all(
                [
                    letter in string.ascii_letters + string.digits + "'"
                    for letter in stripped_end_line.split()[0]
                ]
            )
        ):
            line += (" " + stripped_end_line)

            excluded.append(i + 1)
        # end if

        new_lines.append(line)
    # end for

    output = "\n".join(new_lines)

    lines = output.split("\n")
    new_lines = []
    openings = [f"{opener} " for opener in openers]
    endings = [f"{closer}, " for closer in closers] + ["', '"]

    for line in lines:
        for opener in openings:
            if (
                (opener in line) and
                (not line.endswith(opener)) and
                (not (line.find('"')) < line.find(opener) < line.rfind('"'))
            ):
                line = line.replace(
                    opener, opener.replace(
                        " ", "\n" + ("\t" * (line.replace("    ", "\t").count("\t") + 1))
                    )
                )

                break
            # end if
        # end for

        for ending in endings:
            if (
                (ending in line) and
                (not line.endswith(ending)) and
                (not (line.find('"') < line.find(ending) < line.rfind('"')))
            ):
                line = line.replace(
                    ending, ending.replace(
                        " ", "\n" + ("\t" * (line.replace("    ", "\t").count("\t")))
                    )
                )

                break
            # end if
        # end for

        new_lines.append(line)
    # end for

    return "\n".join(new_lines).replace("    ", "\t").replace("\t ", "\t")
# end indent