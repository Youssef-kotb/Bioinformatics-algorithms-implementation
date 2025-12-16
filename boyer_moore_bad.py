def boyer_moore_bad_char(text, pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == text[i+j]:
            j -= 1

        if j < 0:
            return i
        else:
            shift = j - bad_char.get(text[i+j], -1)
            i += max(1, shift)
    return -1
