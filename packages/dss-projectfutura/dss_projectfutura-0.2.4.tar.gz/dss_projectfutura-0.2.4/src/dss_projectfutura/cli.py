import sys
from text import TextModel, TextTokenizer

txtok = TextTokenizer()
txmod = TextModel()

if sys.argv[1] == 'train':
    text = ''
    for a in sys.argv[2:]:
        with open(a) as f:
            text += f.read() + '\n'
    print('Text loaded!')

    txtok.adapt(text)
    print('Tokenizer adapted!')
    with open('tokens.dss', 'wb') as f:
        f.write(txtok.dump())
    print('Tokenizer written!')
    tokens = txtok.encode(text, fast=True)
    txmod.train(tokens)
    print('Model trained!')
    with open('model.dss', 'wb') as f:
        f.write(txmod.dump())
    print('Model written!')
elif sys.argv[1] == 'predict':
    with open('tokens.dss', 'rb') as f:
        txtok.load(f.read())
    print('Tokenizer loaded!')
    with open('model.dss', 'rb') as f:
        txmod.load(f.read())
    print('Model loaded!')
    print('---')

    print(sys.argv[2].strip(), end=' ')
    toks = txtok.encode(sys.argv[2].strip())
    for i in range(50):
        prd = txmod.predict(toks)
        if prd is None:
            break
        tok = txtok.decode([prd])
        print(tok, end=' ')
        toks.append(prd)
    print()
elif sys.argv[1] == 'complete':
    with open('tokens.dss', 'rb') as f:
        txtok.load(f.read())
    print('Tokenizer loaded!')
    with open('model.dss', 'rb') as f:
        txmod.load(f.read())
    print('Model loaded!')
    print('---')

    while True:
        toks = txtok.encode(input('> ').strip())
        print(txtok.decode(toks), end=' ')
        for i in range(4096):
            prd = txmod.predict(toks)
            if prd is None:
                break
            tok = txtok.decode([prd])
            print(tok, end=' ')
            if tok.strip().endswith('.') and i > 15:
                break
            toks.append(prd)
        print()
elif sys.argv[1] == 'chat':
    with open('tokens.dss', 'rb') as f:
        txtok.load(f.read())
    print('Tokenizer loaded!')
    with open('model.dss', 'rb') as f:
        txmod.load(f.read())
    print('Model loaded!')
    print('---')

    while True:
        toks = txtok.encode('<question> ' + input('> ').strip())
        total = ""
        shouldprint = False
        for i in range(4096):
            prd = txmod.predict(toks)
            if prd is None:
                break
            tok = txtok.decode([prd])
            if tok.strip().lower() == '<question>':
                if shouldprint:
                    break
                else:
                    toks.append(prd)
                    continue
            if tok.strip().lower() == '<answer>':
                shouldprint = True
                toks.append(prd)
                continue
            total += tok + ' '
            if shouldprint:
                print(tok, end=' ')
            if tok.strip().endswith('.') and i > 15:
                break
            toks.append(prd)
        if not shouldprint:
            print(total, end='')
        print()

