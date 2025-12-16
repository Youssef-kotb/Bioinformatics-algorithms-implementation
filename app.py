import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import os

from boyer_moore_bad import boyer_moore_bad_char
from complement import complement
from dna_translation import translate_dna
from edit_distance import edit_distance
from gc_precentage import gc_percentage
from hamming_distance import hamming_distance
from overlab_graph import overlap_graph
from read_fasta import read_fasta_multi
from reverse_complement import reverse_complement
from reverse import reverse_seq
from suffix_array import suffix_array, inverse_suffix_array

# ======================
# Global storage
# ======================
fasta_sequences = {}
history = []  # Store history as (sequence_name, operation, result)

# ======================
# Helper functions
# ======================
def get_seq(name):
    return fasta_sequences.get(name, "")

def add_history(operation, result):
    selected_seq = seq_selector_a.get()
    history.append((selected_seq, operation, result))

def show_result(result, operation=None):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, str(result))
    if operation:
        add_history(operation, result)

# ======================
# FASTA handling
# ======================
def import_fasta():
    global fasta_sequences

    file_path = filedialog.askopenfilename(
        title="Select FASTA File",
        filetypes=[("FASTA files", "*.fasta *.fa *.txt")]
    )

    if file_path:
        fasta_sequences = read_fasta_multi(file_path)

        names = list(fasta_sequences.keys())
        seq_selector_a["values"] = names
        seq_selector_b["values"] = names

        if names:
            seq_selector_a.current(0)
            seq_selector_b.current(0)

        update_sequence_display()

def update_sequence_display(event=None):
    seq_text.delete(1.0, tk.END)
    selected = seq_selector_a.get()
    if selected:
        seq_text.insert(tk.END, get_seq(selected))

# ======================
# Algorithm actions
# ======================
def run_gc():
    seq = get_seq(seq_selector_a.get())
    result = f"GC Percentage: {gc_percentage(seq):.2f}%"
    show_result(result, "GC Percentage")

def run_reverse():
    seq = get_seq(seq_selector_a.get())
    result = reverse_seq(seq)
    show_result(result, "Reverse")

def run_complement():
    seq = get_seq(seq_selector_a.get())
    result = complement(seq)
    show_result(result, "Complement")

def run_reverse_complement():
    seq = get_seq(seq_selector_a.get())
    result = reverse_complement(seq)
    show_result(result, "Reverse Complement")

def run_translation():
    seq = get_seq(seq_selector_a.get())
    result = translate_dna(seq)
    show_result(result, "DNA Translation")

def run_boyer_moore():
    text = get_seq(seq_selector_a.get())
    pattern = get_seq(seq_selector_b.get())
    index = boyer_moore_bad_char(text, pattern)
    if index == -1:
        result = "Pattern not found"
    else:
        result = f"Pattern found at index {index}"
    show_result(result, "Boyer–Moore Search")

def run_hamming():
    s1 = get_seq(seq_selector_a.get())
    s2 = get_seq(seq_selector_b.get())

    if len(s1) != len(s2):
        messagebox.showerror(
            "Error",
            "Hamming Distance requires sequences of equal length"
        )
        return

    result = f"Hamming Distance: {hamming_distance(s1, s2)}"
    show_result(result, "Hamming Distance")

def run_edit_distance():
    s1 = get_seq(seq_selector_a.get())
    s2 = get_seq(seq_selector_b.get())
    result = f"Edit Distance: {edit_distance(s1, s2)}"
    show_result(result, "Edit Distance")

def run_suffix_array():
    seq = get_seq(seq_selector_a.get())
    sa = suffix_array(seq)
    result = f"Suffix Array:\n{sa}"
    show_result(result, "Suffix Array")

def run_inverse_suffix_array():
    seq = get_seq(seq_selector_a.get())
    sa = suffix_array(seq)
    isa = inverse_suffix_array(sa)
    result = f"Inverse Suffix Array:\n{isa}"
    show_result(result, "Inverse Suffix Array")

def run_overlap_graph():
    reads = list(fasta_sequences.values())
    graph = overlap_graph(reads, min_length=2)

    result = ""
    for k, v in graph.items():
        result += f"{k[:10]}... -> {v}\n"
    if not result:
        result = "No overlaps found"
    show_result(result, "Overlap Graph")

# ======================
# History management
# ======================
def save_history():
    if not history:
        messagebox.showinfo("Info", "History is empty. Nothing to save.")
        return

    filename = simpledialog.askstring("Save History", "Enter file name (without extension):")
    if filename:
        if not filename.endswith(".txt"):
            filename += ".txt"
        if not os.path.isdir('outputs'):
            os.mkdir('outputs')
        file_path = os.path.join(os.getcwd(), 'outputs', filename)
        with open(file_path, "w") as f:
            for seq_name, operation, result in history:
                f.write(f">{seq_name} -> {operation} ->{result}\n")
        messagebox.showinfo("Saved", f"History saved to {file_path}")

def clear_history():
    if not history:
        messagebox.showinfo("Info", "History is already empty.")
        return

    confirm = messagebox.askyesno(
        "Confirm Clear History",
        "Do you want to clear the history?\nNote: the history is permanently deleted."
    )
    if confirm:
        history.clear()
        messagebox.showinfo("Cleared", "History has been cleared.")

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Bioinformatics Sequence Analyzer")
root.geometry("820x700")
root.configure(bg="#f4f6f8")

# ---------- Title ----------
tk.Label(
    root,
    text="Bioinformatics Sequence Analyzer",
    font=("Helvetica", 20, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
).pack(pady=(20, 5))

tk.Label(
    root,
    text="Import FASTA files, select sequences, and apply bioinformatics algorithms.",
    font=("Helvetica", 11),
    bg="#f4f6f8",
    fg="#555"
).pack(pady=(0, 20))

# ---------- Import ----------
tk.Button(
    root,
    text="Import FASTA File",
    font=("Helvetica", 11, "bold"),
    bg="#3498db",
    fg="white",
    padx=18,
    pady=6,
    command=import_fasta
).pack(pady=10)

# ---------- Sequence selectors ----------
selectors = tk.Frame(root, bg="#f4f6f8")
selectors.pack(pady=10)

tk.Label(selectors, text="Sequence A:", bg="#f4f6f8").grid(row=0, column=0, padx=5)
seq_selector_a = ttk.Combobox(selectors, state="readonly", width=135)
seq_selector_a.grid(row=0, column=1, padx=5)
seq_selector_a.bind("<<ComboboxSelected>>", update_sequence_display)

tk.Label(selectors, text="Sequence B:", bg="#f4f6f8").grid(row=1, column=0, padx=5)
seq_selector_b = ttk.Combobox(selectors, state="readonly", width=135)
seq_selector_b.grid(row=1, column=1, padx=5)

tk.Label(
    selectors,
    text="(Used only for algorithms requiring two sequences)",
    bg="#f4f6f8",
    fg="#777",
    font=("Helvetica", 9)
).grid(row=2, column=1, sticky="w", pady=(2, 0))

# ---------- Sequence display ----------
seq_text = tk.Text(
    root,
    height=10,
    width=95,
    font=("Courier New", 10),
    wrap=tk.WORD
)
seq_text.pack(pady=15)

# ---------- Algorithms ----------
algo_frame = tk.LabelFrame(
    root,
    text="Algorithms",
    font=("Helvetica", 11, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50",
    padx=10,
    pady=10
)
algo_frame.pack(pady=10)

# Row 0
tk.Button(algo_frame, text="GC Percentage", width=22, command=run_gc).grid(row=0, column=0, padx=5, pady=5)
tk.Button(algo_frame, text="Reverse", width=22, command=run_reverse).grid(row=0, column=1, padx=5, pady=5)
tk.Button(algo_frame, text="Complement", width=22, command=run_complement).grid(row=0, column=2, padx=5, pady=5)

# Row 1
tk.Button(algo_frame, text="Reverse Complement", width=22, command=run_reverse_complement).grid(row=1, column=0, padx=5, pady=5)
tk.Button(algo_frame, text="DNA Translation", width=22, command=run_translation).grid(row=1, column=1, padx=5, pady=5)
tk.Button(algo_frame, text="Suffix Array", width=22, command=run_suffix_array).grid(row=1, column=2, padx=5, pady=5)

# Row 2
tk.Button(algo_frame, text="Inverse Suffix Array", width=22, command=run_inverse_suffix_array).grid(row=2, column=0, padx=5, pady=5)
tk.Button(algo_frame, text="Boyer–Moore Search", width=22, command=run_boyer_moore).grid(row=2, column=1, padx=5, pady=5)
tk.Button(algo_frame, text="Overlap Graph", width=22, command=run_overlap_graph).grid(row=2, column=2, padx=5, pady=5)

# Row 3
tk.Button(algo_frame, text="Hamming Distance", width=22, command=run_hamming).grid(row=3, column=0, padx=5, pady=5)
tk.Button(algo_frame, text="Edit Distance", width=22, command=run_edit_distance).grid(row=3, column=1, padx=5, pady=5)

# ---------- History buttons ----------
history_frame = tk.Frame(root, bg="#f4f6f8")
history_frame.pack(pady=10)
tk.Button(history_frame, text="Save History", width=22, bg="#2ecc71", fg="white", command=save_history).grid(row=0, column=0, padx=10)
tk.Button(history_frame, text="Clear History", width=22, bg="#e74c3c", fg="white", command=clear_history).grid(row=0, column=1, padx=10)

# ---------- Output ----------
tk.Label(root, text="Output:", bg="#f4f6f8").pack()
output_text = tk.Text(root, height=6, width=95)
output_text.pack(pady=(5, 15))

# ---------- Footer ----------
tk.Label(
    root,
    text="Bioinformatics GUI Application",
    font=("Helvetica", 9),
    bg="#f4f6f8",
    fg="#888"
).pack(side=tk.BOTTOM, pady=10)

root.mainloop()
