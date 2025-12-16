def read_fasta_multi(filename):
    sequences = {}
    current_name = None
    current_seq = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_name:
                    sequences[current_name] = "".join(current_seq)
                current_name = line[1:]
                current_seq = []
            else:
                current_seq.append(line)

        if current_name:
            sequences[current_name] = "".join(current_seq)

    return sequences
