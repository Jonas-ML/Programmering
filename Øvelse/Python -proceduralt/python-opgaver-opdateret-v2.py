"""""
 OPG 5.1
forNavn = input("fornavn")
efterNavn = input("efternavn")
resultat = forNavn + ", " + efterNavn
print(resultat)

 OPG 5.4
navn = input("navn")
print(navn.upper())
print(navn.lower())

 OPG 5.5
fullName = input("fullName")
print(fullName.title())

 OPG 5.7
number = input()
number2 = input()
number = int(number)
number2 = int(number2)
sum = number + number2
gennemsnit = (number + number2) / 2
print(sum)
print(gennemsnit)

 OPG 5.8
navn = input("navn")
alder = input("alder")

print(navn + " , " + alder + " år")

 OPG 5.9
mil = 1609
afstand = input("afstand")
afstand=int(afstand)
resultat = mil * afstand
print(resultat, end=" meter")

 OPG 5.10 og 5.11
fag=[]
fag.insert(0, "programmering")
   fag.append("indlejrede systemer")
   fag.append("virksomhed")
   fag.append("netværksteknologi")

antalFag = len(fag)
print(fag)
print(antalFag, end=" fag" )

OPG 5.13

lokation = input("By")
indbyggerTal = input("Indbyggertal")
print(lokation + " by , " + indbyggerTal, end=" indbyggere")

OPG 5.14

fag1 = input("karakter1")
fag2 = input("karakter2")
fag3 = input("karakter3")

fag1 = int(fag1)
fag2 = int(fag2)
fag3 = int(fag3)

sum1 = fag1 / 4
sum2 = fag2 / 4
sum3 = fag3 / 2

resultat = sum1+sum2+sum3 / 3

print(resultat, end="  karakterGennemsnit")


OPG 5.15
matematik = ["Matematik", 7]
dansk = ["Dansk", 12]

mineKarakterer = [matematik, dansk]

print(mineKarakterer)


OPG 5.16
mineKarakterer = []
primFag = []
sekuFag = []


fag1 = input("fag1")
karakter1 = int(input("karakter1"))
primFag.insert(0, fag1)
primFag.insert(1, karakter1)

fag2 = input("fag2")
karakter2 = int(input("karakter2"))
sekuFag.insert(0, fag2)
sekuFag.insert(1, karakter2)


mineKarakterer.insert(0, primFag)
mineKarakterer.append(sekuFag)
print(mineKarakterer)

resultat = karakter1+karakter2
print(resultat/2, end=" karakterGennemsnit")


OPG 6.1
lande = ["Danmark", "Tyskland", "Italien", "Norge", "Sverige"]

for lande in lande:
    print(lande)


OPG 6.2
sprog = {"python", "C", "C++", "js"}

for sprog in sprog:
    print(sprog, end=" , ")


"""""
#OPG 6.3 - brug range funktionen til at udskrive tal
#end bruges til at udskrive dem på sammen linje adskilt af et komma

"""""
liste= list(range(0, 31, 3))
for n in liste:
    print(n, end=",")

a = list(range(0, 110, 10))
for a in a:
    print(a, end=",")

b = list(range(-36, 42, 6))
for b in b:
    print(b)

c = list(range(1, 10))
for c in c:
    print(c*c)

d=list(range(1,10))
 
"""""


"""""
# OPG 6.5 printer de første 5 tal fra listen

liste= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

firstFive = liste[0:5]
print(firstFive)

"""
"""""
#OPG 6.6 printer de sidste 5
liste= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

lastFive = liste[5:10]
print(lastFive)

""""""""

#OPG 6.6a printer 4,5,6
liste= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
midThree = liste[4:7]
print(midThree)

""""""""

#OPG 6.7 - printer maximum og minimum, vha indbygget funktion i python
liste = [2, 5, 6, 11, 8, 9, 22]
print("maximum:", max(liste))
print("minimum:", min(liste))

""""""""

#OPG 6.8 - tester pågældene udsagn

a = 2
b = 4
c = 6

print("a) er ",end="")
if a==4 or b>2:
    print("sand")
else:
    print("falsk")


print("b) er ",end="")
if 6<=c and a>3:
    print("sand")
else:
    print("falsk")


print("c) er ",end="" )
if not(a>2):
    print("sand")
else:
    print("falsk")

print("d) er ",end="")
if 1!=b and c!=3:
   print("sand")
else:
   print("falsk")

print("e) er ",end="")
if a>=-1 or a<=b:
   print("sand")
else:
   print("falsk")

print("f) er ",end="")
if not(c==6 and not(a>=b)):
   print("sand")
else:
   print("falsk")

""""""""

#OPG 6.9 - gæt et tal
antalForsoeg = 5
hemmeligtTal = 2
for n in range(0, antalForsoeg):
    sTal=input("Skriv et tal: ")
    tal=int(sTal)
    if (tal == hemmeligtTal):
        print("Du har gættet rigtigt!!")
        break;
    else:
        print("Forkert, prøv igen")

""""""""

#OPG 6.10 a - b og c


iAlder =input("hvad er din alder?")
kategorier = []

alder =int(iAlder)



if alder<=3:
    print("Baby")
elif alder <=12:
    print("Barn")
elif alder<=17:
    print("Teenager")
elif alder<=64:
    print("voksen")
else:
    print("pensionist")

kategorier.append(iAlder)
print(kategorier)


#OPG 6.11 - giver brugeren unlimited inputs og gemmer i en liste som printes ved at trykke enter


inputs = []

while True:
    inp = input("skriv de bynavne du kan - enter for stop")
    if inp =="":
        break
    inputs.append(inp)


print(inputs)



#OPG 6.12 - lader brugeren vælge antal input og printer dem derefter i en liste
antalForsoeg = int(input("deklarer antal forsøg"))
bynavne = []
for n in range(0, antalForsoeg):
    bynavn = input("skriv et bynavn")
    bynavne.append(bynavn)

print(bynavne, "Dine inputs")


#OPG 6.13
antalTal = int(input("antal tal"))
talListe = []
for n in range(0, antalTal):
    tal = int(input("skriv et tal"))
    talListe.append(tal)


print("Dine tal:", talListe)
print("summen af dine tal", sum(talListe))
print("maximum:", max(talListe))
print("Minimum", min(talListe))

gennemsnit = sum(talListe)/len(talListe) # indbyggede funktioner til summen af liste og længden
print(gennemsnit)


#OPG 6.14
bilKategorier = []
kategori1 = ["Tesla, 550000"]
kategori2 = ["BMW, 250000"]
kategori3 = ["Audi, 400000"]

bilKategorier.append(kategori1)
bilKategorier.append(kategori2)
bilKategorier.append(kategori3)

#printer hver kategori på ny linje
for kategori in bilKategorier:
    for x in kategori:
        print(x)





#OPG 6.15
talListe = []
while True:
    inp = input("Skriv dine tal - ent for ext")
    if inp =="":
        break
    talListe.append(inp)


lisorted = sorted(talListe)
print(lisorted)

""""""""
#OPG 6.16

slik = []
vogn =[]
slik1 = ["Mars,7 KR"]
slik2 = ["Twix, 5 KR"]
slik3 = ["Bounty, 8 KR"]
slik.append(slik1)
slik.append(slik2)
slik.append(slik3)
print(slik) 


while True:
    inp = input("vælg slik, tryk s for sum")
    if inp == "":
        break
    if inp == "m":
        vogn.append(int(7))
    if inp == "t":
        vogn.append(int(5))
    if inp == "b":
        vogn.append(int(8))
    if inp == "s":
        print("total, DKK", sum(vogn))



#OPG 6.17 - mangler


#OPG 7.1 - printer først de første 3 navne og derefter de sidste 3

navne = ["allan", "peter", "mads", "jens", "bent", "jannik"]
navneS = sorted(navne)
print(navne[ :3])
print(navne[3:])


#OPG 7.2 - gæt et tal med indikation alt efter for høj/lav
forsoeg = 5
rigtigeTal = 3
for n in range(0, forsoeg):
    tal = int(input("Gæt et tal"))
    if tal == rigtigeTal:
        print("Rigtigt!!")
    if tal > rigtigeTal:
        print("Du er lidt for højt, prøv igen")
    if tal < rigtigeTal:
        print("Du er lidt for lavt, prøv igen")
    

#OPG 7.3 - se OPG 6.10


#WIP - kan gemme i listerne dog ikke globalt ######################################################################################

alder =int(input("hvad er din alder?"))
kategorier = []
baby = [0,3, "baby, din alder"]
barn = []

if alder<=3:
    print("Baby")
    baby.append(alder)
elif alder <=12:
    print("Barn")
    barn.append(alder)
elif alder<=17:
    print("Teenager")
elif alder<=64:
    print("voksen")
else:
    print("pensionist")

kategorier.append(baby)
kategorier.append(barn)
print(kategorier)

""""""""

#OPG 7.4 

antalForsoeg = int(input("deklarer antal forsøg"))
bynavne = []
for n in range(0, antalForsoeg):
    bynavn = input("skriv et bynavn")
    bynavne.append(bynavn)

print(bynavne, "Dine inputs")



byListe = []
while True:
    bynavn = input("bynavne/enter for at slutte")
    if bynavn == "":
        break
    else:
        byListe.append(bynavn)
        print(byListe)
"""

#opg 7.4










#sørens øvelse - liste der printer 0 - 50 i intervaller af 5
#li = list(range(0, 51, 5))
#for n in li:
#    print(n)


# != betyder tal forskellige fra 5
"""""
talListe = [1, 2, 3, 4, 5]

for tal in talListe:
    print(tal)
    if tal ==5:
        break

n = 0
while tal != 5:  
    print(talListe[n])
    n=n + 1






# eks på funktion til udregning
#øverste blok er defineringen af funktionen og blokken nederst er der funktionen bliver kaldt
#rækkefølge er vigtig!!
#variabler defineret i funktioner  er lokale variabler og er derfor uafhængige af de variabler man laver udenfor funktionen

def talSum(a, b):
    total = a + b
    return(total)


#programmet der bruger funktionaliteterne


a = 2
b = 3
c = talSum(a, b)
print(c)

#man kan gemme sine funktioner i en fil for sig og importe dem som vidst til brug

import mineFunktioner
eller import mineFunktioner as f for at forkorte
a = 2 
b = 3
c = mineFunktioner.talSum(a, b)
print(c)

"""
