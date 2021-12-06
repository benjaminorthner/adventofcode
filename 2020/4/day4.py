import re
with open("input.dat", "r") as file:
    lines = [line for line in file.readlines()]

'''
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
'''
items = ["byr", "iyr", "eyr", "hgt","hcl", "ecl", "pid"]
passp = {}
validc = 0
for line in lines:
    line = line.strip()
    
    # if line empty
    if not line:
        valid = True

        for item in items:
            if item not in passp.keys():
                valid = False
        
        if valid:
            if not (1920 <= int(passp['byr']) <= 2002) or not (len(passp['byr']) == 4):
                valid = False
                
            if not (2010 <= int(passp['iyr']) <= 2020) or not (len(passp['iyr']) == 4):
                valid = False
                
            if not (2020 <= int(passp['eyr']) <=2030) or not (len(passp['eyr']) == 4):
                valid = False                
            
            if re.findall("^\d+cm", passp["hgt"]) != []:
                if not (150<= int(re.findall("\d+", passp['hgt'])[0]) <= 193):
                    valid = False                    

            if re.findall("^\d+in", passp["hgt"]) != []:
                if not (59<= int(re.findall("\d+", passp['hgt'])[0]) <= 76):
                    valid = False                    
            
            if re.findall("^#[0-9a-f]{6}$",passp['hcl']) == []:
                valid = False                

            if passp['ecl'] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                valid = False
            
            if re.findall("^\d{9}$",passp["pid"]) == []:
                valid = False

        if valid:
            validc += 1
            
        passp = {}

    # if line not empty
    else:
        words = line.split()
        for word in words:
            k, v = word.split(':')
            passp[k] = v

# off by one for some reason
print(validc-1)
