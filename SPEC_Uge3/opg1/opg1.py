import matplotlib.pyplot as plt
from collections import defaultdict
from wordcloud import WordCloud

names = [
    "Alexander", "Benjamin", "Charlotte", "Daniel", "Emily", "Frederik", 
    "Gabriel", "Hannah", "Isabella", "Jacob", "Katherine", "Liam", "Mia", 
    "Nathan", "Olivia", "Peter", "Quinn", "Rebecca", "Samuel", "Theresa", 
    "Ulysses", "Victoria", "William", "Xander", "Yasmine", "Zachary",
    "Amelia", "Aaron", "Sophia", "Noah", "Ava", "James", "Lucas", "Ethan", 
    "Ella", "David", "Elijah", "Aria", "Jackson", "Aiden", "Scarlett", 
    "Sofia", "Matthew", "Logan", "Abigail", "Grace", "Henry", "Isla", 
    "Ryan", "Evelyn", "Oliver", "Sebastian", "Harper", "Caleb", "Chloe", 
    "Julian", "Penelope", "Levi", "Victoria", "Dylan", "Aurora", "Luke", 
    "Hazel", "Isaac", "Samantha", "Theodore", "Lily", "Grayson", "Lillian", 
    "Joshua", "Layla", "Zoe", "Madison", "Owen", "Caroline", "Leo", 
    "Alice", "Mason", "Eleanor", "Wyatt", "Ellie", "Jack", "Nora", "Lucas",
    "Sarah", "Evan", "Luna", "Mila", "Eli", "Sadie", "Landon", "Addison",
    "Jaxon", "Piper", "Lincoln", "Stella", "Connor", "Grace", "Hudson", 
    "Ruby", "Carson", "Sophia", "Asher", "Kinsley", "Christian", "Brielle",
    "Maverick", "Vivian", "Nolan", "Emilia", "Hunter", "Camila", "Adrian", 
    "Archer", "Easton", "Emery", "Maddox", "Faith", "Roman", "Riley"
]

#Sort by Length
def LenFunc(e):
    return len(e)
#names.sort(key=LenFunc)

#sort alphabetically
#names.sort()
#names.sort(reverse=True)

#print(names)
def dicMaker(names):
    char_dict = defaultdict(lambda: 0)  
    letterString = "abcdefghijklmnopqrstuvwxyzæøåABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"
    for char in letterString:
        char_dict[char]
    
    for name in names:
        for char in name:
            if char_dict[char] == "0":  
                char_dict[char] = 1
            else: 
                amount = int(char_dict[char])  
                amount += 1
                char_dict[char] = amount 
    
    return char_dict
letter_dict = dicMaker(names=names)

#print(letter_dict)

def plothist():
    x = list(letter_dict.keys())
    y = [int(val) for val in letter_dict.values()]  
    plt.bar(x,y)
    
    plt.xlabel("Bogstaver")
    plt.ylabel("Antal forekomster")
    plt.title("Plz work")
    
    plt.show()

plothist()

wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(letter_dict)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # Turn off axis
plt.show()