import random
import lists


def update_dnf(book):
    lists.dnf_list.append(book)
    print(f"{book} has been added to your 'Did Not Finish' list. 📚🚫")

def update_book_List(book):
    lists.list1.remove(book)
    print(f"{book} has been removed from your book list. 📚🚫")


def show_next_book():
    if lists.list1:
        book = random.choice(lists.list1)  # Pick a random book
        lists.list1.remove(book)  # Remove it from the list
        phrase = random.choice(lists.list2)  # Random phrase for the next book
        print(phrase + book)
    else:
        print("You've read all your books! Time to add more! 📚🔥")

book_choice = input("Hey Andrea did you finish reading your current book (yes/no): ")

if book_choice == 'yes':
    finished_book = input("Which book did you finish reading? ")
    update_book_List(finished_book)
    next_book = input('Are you ready for your next book: ')
    if next_book == 'yes':
        print(lists.next_book_phrases + lists.book_list)
    else:
        print('Come back next time when you are ready')
elif book_choice == 'no':
    current_book = input("Which book are you still reading? ")
    still_reading = input(f"Are you still reading {current_book}? (yes/no): ")
    if still_reading == 'yes':
        print(lists.words_of_affirmation)
    elif still_reading == 'no':
         update_dnf(current_book)  # Move the book to the DNF list
         next_book = input('Are you ready for your next book (yes/no)? ')
         if next_book.lower() == 'yes':
            show_next_book()
    
         else:
             print('Come back when you are ready for your next read!!!!')
    else:
        print('Im sorry i dont understand')
else:
    print('Im sorry i dont understand')
    

    
"""
liked_songs = {
    'Luther': 'Kendrick Lamar & SZA',
    'Not Like Us': 'Kendrick Lamar',
    'Die With A Smile': 'Lady Gaga & Bruno Mars',
    'TV Off': 'Kendrick Lamar featuring Lefty Gunplay',
    '4x4': 'Travis Scott',
    'Pink Pony Club': 'Chappell Roan',
    '30 for 30': 'SZA with Kendrick Lamar',
    'Gimme a Hug': 'Drake',
    'Nokia': 'Drake'
}

def write_liked_songs_to_file(songs, 'liked songs.txt'):
  with open('liked songs.txt', 'w') as w:
    for song, artist in songs.item():
      w.write(f"{song} by {artist}\n")
"""
      