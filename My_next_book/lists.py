import random

# List of books
list1 = ['book1', 'book2', 'book3', 'book4']

# List of phrases for the next book
list2 = [
    "Your next literary conquest will be 👑📖: ",
    "Up next in your book-loving saga 🎬📚: ",
    "And the next chapter of your reading adventure is 🚀📖: ",
    "Your next page-turner awaits 🔥📚: ",
    "The book gods have chosen your next quest ⚡📖: ",
    "Next on your making me fall for you even more list 😍📚: ",
    "Drumroll, please... your next victim—I mean, book—is 🥁📖: ",
    "As one book closes, another one tempts you... next up is 👀📚: ",
    "Destiny (or me) has decided—your next book is 😏📖: ",
    "Coming soon to a cozy reading nook near you 🎥📚: "
]

# List of words of affirmation
list3 = [
    'Dale, bebé, that book isnt gonna finish itself! 📖🔥',
    'Every page you turn = +10 to your hotness stat.😏📚',
    'Youre too deep in now-no quitting like a novela character! 🎭📖',
    'Finish that book so I can hype you up properly! 🚀📖',
    'One more chapter, and I promise you the best You did it! hug ever. 🤗📚',
    'Books and brains? Youre making it hard to focus, mujer. 😏📖',
    'Read now, cuddle later. Best deal ever. 😘📚',
    'You finish that book, and Ill plan the celebration—food, drinks, lo que quieras. 🍷📖',
    'Youre making this book look good, but you look even better reading it. 😍📖'
]

# DNF (Did Not Finish) list
dnf_list = []

book_list = random.choice(list1)
next_book_phrases = random.choice(list2)
words_of_affirmation = random.choice(list3)