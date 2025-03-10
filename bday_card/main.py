import datetime
import bday_message

today = datetime.date.today()
next_birthday = datetime.date(2025,3,7)


days_away = next_birthday - today

if next_birthday == today:
  print(bday_message.random_message)
else:
  print(f'My next birthday is {days_away.days} days away!')