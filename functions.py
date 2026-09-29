

#Reference Function
def clean_name(name):
    cleaned = name.strip().lower()
    return cleaned

cln_name = clean_name(" maRia  ")
print(cln_name)
#Odd or Even
def is_even(num):
    if num%2 == 0:
        return True
    else:
        return False

in_num = is_even(78)
print(in_num)


#Prime number check

    
def is_prime(num):
    for i in range(2,num):
        if num % i == 0:
            return False
            
    else:
        return True
in_num = is_prime(99)
print(in_num)


#Sum of digits
def sum_digits(num):
    total = 0
    while num>0:
        digit = num % 10
        total += digit
        num = num // 10
    return total
enter_no = sum_digits(123)
print(enter_no)

#multiply the digits
def multiply(a, b=2):
    return a*b
in_num = multiply(2,8)
print(in_num)

