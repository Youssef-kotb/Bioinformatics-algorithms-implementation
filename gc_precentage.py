def gc_percentage(seq):
    gc = seq.count('G') + seq.count('C')
    return (gc / len(seq)) * 100
