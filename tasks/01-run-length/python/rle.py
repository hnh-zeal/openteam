def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    # TODO: implement

    if not s:
        return ""
    
    count = 1
    result = []
    current_char = s[0]

    for ch in s[1:]:
        if ch == current_char:
            count += 1
        else:
            result.append(f"{current_char}{count}")
            count = 1
            current_char = ch
    
    # Append the last item
    result.append(f"{current_char}{count}")
    return ''.join(result)

