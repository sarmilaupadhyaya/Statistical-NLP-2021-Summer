# No idea what else we'd need to change

with open("data/alice_in_wonderland.txt", "r") as f:
    a = [char for char in f.read().lower()]
    exercise_3.analysis("English", a)
    
with open("data/alice_im_wunderland.txt", "r") as f:
    a = [char for char in f.read().lower()]
    exercise_3.analysis("German", a)
    
with open("data/torch_activation.py", "r") as f:
    tokens = [
        x.string
        for x in tokenize.generate_tokens(f.readline)
        if x.type not in {
            tokenize.COMMENT, tokenize.STRING, tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE
        }
    ]
    a = [char for char in tokens] # this might be wrong
    exercise_3.analysis("Python", a)
