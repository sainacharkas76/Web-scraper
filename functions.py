import os

def medline_formatting(medline_string):

    medline_list = medline_string.split('\n')

    ls = []
    for elem in medline_list:
        if elem == '':
            continue
        elif elem[0:4] != '    ':
            elem = elem.strip()
            elem = elem.replace('\n', '')
            ls.append(elem)
        else:
            elem = elem.strip()
            elem = elem.replace('\n', '')
            ls[-1] = ls[-1] + ' ' + elem
    
    ls_2 = [] 
    for elem in ls:
        key = elem[0:4].strip()
        value = elem[5:].strip()
        
        ls_2.append([key, value])

    return ls_2

def progress_bar(value,tot):

    perc = value/tot*100

    bar = [x for x in range(0,100,5)]
    index = sum(1 for i in bar if i < perc)
    bar = '[' + '='*index + ' '*(20-index) + '] ' + str(round(perc,1)) + '%'
    os.system('cls' if os.name=='nt' else 'clear')
    
    print('Retrieving data from ' + str(tot) + ' papers')
    print(bar)

def request_words():
    print('Building a dictionary')
    ls = []
    while True:
        word = input('Please insert a word (quit to stop): ')
        if word == 'quit':
            break
        else:
            ls.append(word)

    return ls

def process_text(text):
    if text == None:
        return 
    text = text.strip()
    text = text.lower()
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace(':', ' ')
    text = text.replace(';', ' ')
    text = text.replace('*', ' ')
    text = text.replace('/', ' ')
    text = text.replace('-', ' ')
    text = text.replace('&', ' ')
    text = text.replace('=', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace("'", ' ')
    text = text.replace("<", ' ')
    text = text.replace(">", ' ')
    return text

def count_words(text, dictionary):
    text = process_text(text)
    text = text.split()
    for word in text:
        if word not in dictionary:
            dictionary[word] = 0
        dictionary[word] += 1
    return dictionary

def compute_score(df, dictionary):
    titles = df['Title'].tolist()
    abstracts = df['Abstract'].tolist()
    keywords = df['Keywords'].tolist()
    scores = []
    for i in range(len(titles)):
        score = 0
        try:
            title_occ = count_words(titles[i], {})
            abst_occ = count_words(abstracts[i], {})
            keys_occ = count_words(keywords[i], {})
        except:
            scores.append(0)
            continue
        
        for word in dictionary:
            if word in title_occ:
                score = score + title_occ[word]*3
            if word in abst_occ:
                score = score + abst_occ[word]
            if word in keys_occ:
                score = score + keys_occ[word]*3
        
        scores.append(score)
    scores = [(i-min(scores))/(max(scores)-min(scores)) for i in scores]
    scores = [round(i, 2) for i in scores]
    return scores
