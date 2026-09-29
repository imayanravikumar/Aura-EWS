
print("meow\n" * 4, end="")

while True:
    n = int(input("Whatsn? "))
    if n < 0:
        continue
    else:
        break

while True:
    n = int(input("Whats n? "))
    if n > 0:
        break


for _ in range(n):
    print("mewo")
     
def main():
    number = get_number()
    meow(number)

def get_number():
    while True:
        n = int(input("Whats n?"))
    if n > 0:
        return n
def meow(n):
    for _ in range(n):
        print("meaw")

num = int(input("enter a number "))
last_digit = num%10
print(last_digit)

for i in (1,2,3):
    print(i)


for i in (1,2,3,4,5):
    print("Round: 1")
#printing the 7 table 
for t in range(1,11):
    print(f"7 x {t} = {t*7}")


#printing the right angled triangle
for i in range(1,8):
    
    print("*"*i)


#finding duplicate files 
files = [
    'report.csv',
    'data..xlsx',
    'summary.docx',
    'report.pdf',
    'data.csv',
    ]

seen = set()

for file in files:
    if file in seen:
        print("Duplicate found")
        break
    seen.add(file)
    
else:
        print("All files are unique")







#adding the numbers 
num = int(input("Enter the number: "))
total = 0
while num > 0:
    digit = num  % 10
    total += digit
    num = num // 10
    print(total)


#reverse the numbers

num = int(input("Enter the number: "))
reverse = 0

while num>0:
    di = num % 10
    reverse = reverse*10+di
    num = num // 10
print(reverse)



#checking if the number is prime


num = int(input("Enter the number: "))

for i in range(2,num):
    if num % i == 0:
        print("It is not a prime number")
        break
else:
    print("It is a prime number")

    
