import random

# List of books
list1 = [ 'x',
    'The Housemaid',
    'The Mysterious Case of the Alperton Angels',
    'Butcher & Blackbird',
    'The Reappearance of Rachel Price',
    'Two Sides to Every Murder',
    'W0rldtr33 Vol. 2',
    'Horror Movie',
    'Spiral',
    'Loop',
    'Ring',
    'The Only Good Indians',
    'The Boyfriend',
    'Their Vicious Games',
    'One By One',
    'The September House',
    'Assistant to the Villain',
    'Home is Where the Bodies Are',
    'Wrong Place Wrong Time',
    'The 7 1/2 Deaths of Evelyn Hardcastle',
    'The Perfect Marriage',
    'Pretty Girls',
    'The Thursday Murder Club',
    'Verity',
    'Tell Me What You Did',
    'Black Chalk',
    'Strange Picture'
]

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