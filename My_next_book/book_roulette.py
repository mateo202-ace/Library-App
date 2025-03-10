import random
import lists



book_choice = input("Hey Andrea did you finish reading your current book: ")

if book_choice == 'yes':
    next_book = input('Are you ready for your next book: ')
    if next_book == 'yes':
        print(lists.next_book_phrases + lists.book_list)
    else:
        print('Come back next time when you are ready')
elif book_choice == 'no':
    print(lists.words_of_affirmation)
else:
    print('Im sorry i dont understand')
    

    

