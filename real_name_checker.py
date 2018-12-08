import nltk
from nameparser.parser import HumanName
from nltk.corpus import wordnet


def is_real_name(username):
    username = username.replace('_', ' ').replace('-', ' ')

    username_list = []
    real_name = username_list
    name_list = []
    name = ''

    token = nltk.tokenize.word_tokenize(username)
    pos = nltk.pos_tag(token)
    category = nltk.ne_chunk(pos, binary=False)

    # Only choose ones with PERSON attribute, and append it to the list
    for subtree in category.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            name_list.append(leaf[0])
        if name_list:
            for word in name_list:
                name += word + ' '
            if name[:-1] not in username_list:
                username_list.append(name[:-1])
            name = ''
        name_list = []

    # Removing common English words categorised as real names
    for user in username_list:
        user_split = user.split(' ')
        for name in user_split:
            if wordnet.synsets(name):
                if name in user:
                    real_name.remove(user)
                    break

    # Checking if there is any real name in the list & returning bool
    return bool(real_name)


if __name__ == '__main__':
    username = input('Enter username: ')
    if is_real_name(username):
        print('Get a new username')
    else:
        print('Nice one')
