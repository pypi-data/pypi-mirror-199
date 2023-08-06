import socket
import requests

def factorial(number):
    fact = 1
    if number < 0:
        print("Factorial for negative numbers don't exist...")
    else:
        for i in range(1,number+1):
            fact = fact*i
            i = i+1
    return fact


def armstrong(number):

    sum = 0

    tempoarary = number
    while tempoarary > 0:
        remainder = tempoarary % 10
        sum += remainder ** 3
        tempoarary //= 10

    if number == sum:
        return True
    else:
        return False


def decimal(binary):
    decimal,i,n = 0,0,0
    while (binary != 0):
        remainder = binary % 10
        decimal = decimal + remainder * 2 ** i
        binary = binary // 10
        i = i+1
    return decimal


def binary(decimal):
    bin = 0
    ctr = 0
    temp = decimal  #copy input decimal
    #find binary value using while loop
    while(temp > 0):
         bin = ((temp%2)*(10**ctr)) + bin
         temp = int(temp/2)
         ctr += 1
    return bin


def peterson(n): 
    num = n 
    sum_val = 0
    while n > 0: 
        digit = int(n % 10) 
        sum_val += factorial(digit) 
        n = int(n / 10) 
    if num==sum_val:
        return True
    else:
        return False

def primeFactors(n):
    if n < 4:
        return n
    arr = []
    while n > 1:
        for i in range(2, int(2+n//2)):
            if i == (1 + n // 2):
                arr.append(n)
                n = n // n
            if n % i == 0:
                arr.append(i)
                n = n // i
                break
    return arr

def perfectSquare(x):
       if(x >= 0):
           #sr = int(math.sqrt(x))
           sr = x**0.5
           return ((sr*sr) == x)
       return False

#finding sine from lengths
def basicSin(p,h):
    sin = p/h
    return sin

#finding cos from lengths
def basicCos(b,h):
    cos = b/h
    return cos

#finding tan from lengths
def basicTan(p,b):
    tan = p/b
    return tan

#finding radian of an angle
def radian(angle):
    rad = angle * (3.141/180)
    return rad

#finding sin function
def sinA(angle):
    rad = radian(angle)
    #print (rad)
    sine = (2.718281828459045**(rad*1j)).imag
    return sine

#finding cos of an angle
def cosA(angle):
    rad = radian(angle)
    #print (rad)
    coss = (2.718281828459045**(rad*1j)).real 
    return coss

#finding tan of an angle
def tanA(angle):
    tan = (sinA(angle)) / (cosA(angle))
    return tan

#finding cosec of an angle
def cosecA(angle):
    cosec = 1/(sinA(angle))
    return cosec

#finding sec of an angle
def secA(angle):
    sec = 1/(cosA(angle))
    return sec

#finding cot of an angle
def cotA(angle):
    cot = (cosecA(angle)) / (secA(angle))
    return cot

#perimeter of a rectangle
def periRectangle(length,width):
    perimeter = 2*(length+width)
    return perimeter

#perimeter of a square
def periSquare(sides):
    perimeter = 4*sides
    return perimeter

#perimeter of a triangle
def periTriangle(a,b,c):
    perimeter = a+b+c
    return perimeter

#circumference of a circle
def circumCircle(radius):
    circumference = 2 * 3.141592653589793238 * radius
    return circumference

#area of a rectangle
def areaRectangle(length, width):
    area = length*width
    return area

#area of a square
def areaSquare(side):
    area = side ** 2
    return area

#area of a triangle
def areaTriangle(base, height):
    area = (base * height)/2
    return area

#radius of a circle
def radiusCircle(circumference):
    radius = (circumference)/(2 * 3.141592653589793238)
    return radius

#basic integration
def basicIntegrate(N, a, b):
    def f(x):
        return x**2
    value = 0
    value2 = 0
    for n in range(1,N+1):
        value += f(a+((n-(1/2)) * ((b-a)/N)))
    value2 = ((b-a)/N) * value
    return value2

#sin integration
def sinIntegration(N, a, b):
    def f(x):
        return (2.718281828459045**(x*1j)).imag
    value = 0
    value2 = 0
    for n in range(1,N+1):
        value += f(a+((n-(1/2)) * ((b-a)/N)))
    value2 = ((b-a)/N) * value
    return value2

#cos integration
def cosIntegration(N, a, b):
    def f(x):
        return (2.718281828459045**(x*1j)).real 
    value = 0
    value2 = 0
    for n in range(1,N+1):
        value += f(a+((n-(1/2)) * ((b-a)/N)))
    value2 = ((b-a)/N) * value
    return value2

#finding ip of a host
def get_ip(url):
    #url = "technoindiahooghly.org"
    return (socket.gethostbyname(url))


def get_location(ip):
    ip_address = ip
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

#ip = get_ip('technoindiahooghly.org')
#print(ip)
#print(get_location(ip))

