
import warnings
import winsound
from tkinter import *
from classes import *

warnings.filterwarnings('ignore')

# Create your characters here, e.g. Xiao Ming => XIAOMING = NPC("Xiao Ming")
# Already created for you guys, just edit the name if you want
protagonist =  Protagonist("", "")
XIAOMING = NPC("Xiao Ming")
JUNGCOOK = NPC("JungCook")
ADAMCMITH = NPC("Adam Cmith")
JOHNNYSIN = NPC("Johnny Sin")

DECREASE = "decrease"
INCREASE = "increase"
BIGGER = "bigger"
SMALLER = "smaller"

def createNameFrame(window:Frame, chatFrame:Frame, characterName:str, xLocation:int = 40): # Creates the name box
       shadow1 = Label(window, text=characterName, background="#1f1f1f", foreground="black", font=("roboto", 18), padx=6, pady=6)
       shadow1.place(in_=chatFrame, x=xLocation+5, y=-23)
       shadow2 = Label(window, text=characterName, background="#2e2e2e", foreground="black", font=("roboto", 18), padx=6, pady=6)
       shadow2.place(in_=chatFrame, x=xLocation+4, y=-24)
       shadow3 = Label(window, text=characterName, background="#3b3a3a", foreground="black", font=("roboto", 18), padx=6, pady=6)
       shadow3.place(in_=chatFrame, x=xLocation+3, y=-25)
       nameLabelFrame = Label(window, text=characterName, background="#d1aa73", foreground="black", font=("roboto", 18), padx=5, pady=5, highlightbackground="#A7885C", highlightthickness=2)
       nameLabelFrame.place(in_=chatFrame, x=xLocation, y=-28)

def cleanUp(afterIds:list, dialogueContainer:Label, storyFrame:Frame):
       winsound.PlaySound(None, winsound.SND_PURGE)
       for afterId in afterIds:
              dialogueContainer.after_cancel(afterId)       
       for widget in storyFrame.winfo_children():
              widget.destroy() 

def createScenes(window: Tk, currentFrame: Frame, textImgNameSound: list):
       storyFrame = Frame(window)
       storyFrame.pack(fill=BOTH, expand=True)
       afterIds = []
       def updateDialogue():
              nonlocal currentIndex
              name = textImgNameSound[currentIndex].get("name")
              dialogue = textImgNameSound[currentIndex].get("text")
              imgFilePath = textImgNameSound[currentIndex].get("imgFilePath")
              soundFilePath = textImgNameSound[currentIndex].get("soundFilePath")
              options = textImgNameSound[currentIndex].get("options")
              affectionCheck = textImgNameSound[currentIndex].get("affectionCheck")
              currentFrame.pack_forget() # Remove current frame
              img = PhotoImage(file=imgFilePath) # Some weird gimmick to make the image work
              pictureFrame = Label(storyFrame, image="", border="2", highlightbackground="#A7885C", highlightthickness=2, height=550)
              pictureFrame.image = img
              pictureFrame.config(image=img)
              pictureFrame.pack(side="top", fill="both")
              if (len(options) > 1): # If there are multiple options, show multiple options.
                     for option in options:
                            def updateCurrentIndex(updatedIndex=option.get("nextSceneIndex"), NPC:NPC=option.get("affection").get("affectedNPC") , affectionChange=option.get("affection").get("change") ):
                                   nonlocal currentIndex
                                   currentIndex = updatedIndex
                                   cleanUp(afterIds, dialogueContainer, storyFrame)
                                   if (affectionChange == 'increase'):
                                       print('increasing affection of ' + NPC.getName())
                                       NPC.increaseAffectionLevel()
                                   if (affectionChange =='decrease'):
                                       print('decreasing affection of ' + NPC.getName())
                                       NPC.decreaseAffectionLevel()
                            optionButton = Button(pictureFrame, text=option['text'], borderwidth=1, background="#d1aa73", foreground="black", font=("roboto", 20), command=lambda idx=option: [updateCurrentIndex(idx.get("nextSceneIndex"), idx.get("affection").get("affectedNPC"), idx.get("affection").get("change")), updateDialogue()], padx=2, pady=6)
                            optionButton.pack(fill=X, padx=50, pady=10, expand=TRUE)
              chatFrame = Frame(storyFrame, background="#d1aa73", border="2", highlightbackground="#A7885C", highlightthickness=2, padx=5, pady=5, height=300) # Container for the chat which includes dialogue and continue buttons
              chatFrame.pack(side="bottom", fill="both", expand=TRUE)
              if (name != None and len(name) > 0):
                     createNameFrame(window, chatFrame, name)
              dialogueContainer = Label(chatFrame, text="", height=0, wraplength=860, justify=LEFT, background="#d1aa73", foreground="black", font=("roboto", 16), padx=50, pady=20)
              dialogueContainer.pack(side="left")
              dialogueContainer.config(text="")
              afterIds.clear()
              for i, word in enumerate(dialogue): # Creates the text effect
                     def updateText(w=word):
                            currentText = dialogueContainer.cget("text")
                            dialogueContainer.configure(text=currentText + w)
                     afterId = dialogueContainer.after(20 * i, updateText) # Logs the afterId so I can stop it from running when I go to the next scene
                     afterIds.append(afterId)  # Store the after ID 
              if (soundFilePath != None):
                     winsound.PlaySound(soundFilePath, winsound.SND_ASYNC)
              chatButtonContainer = Frame(chatFrame, background="#d1aa73")
              chatButtonContainer.pack(side="right", fill="both")
              def continueDialogue():
                     nonlocal currentIndex
                     cleanUp(afterIds, dialogueContainer, storyFrame)
                     if (len(options) == 1):
                         currentIndex = options[0]
                     else: 
                         currentIndex += 1
                     updateDialogue()
              def continueDialogueToScene(sceneIndex: int):
                     nonlocal currentIndex
                     cleanUp(afterIds, dialogueContainer, storyFrame)
                     currentIndex = sceneIndex
                     updateDialogue()
              chatButton = Button(chatButtonContainer, text='Continue >>', borderwidth=2, background="#d1aa73", foreground="black", font="roboto", command=continueDialogue, padx=2, pady=2)
              if(affectionCheck != None):
                     affectedNPC: NPC = affectionCheck.get("NPC")
                     comparison = affectionCheck.get("comparison")
                     amount: int = affectionCheck.get("amount")
                     altSceneIndex: int = affectionCheck.get("altSceneIndex")
                     if (comparison == BIGGER):
                            if (affectedNPC.getAffectionLevel() > amount):
                                   chatButton.config(command=continueDialogueToScene(altSceneIndex))
                            else:
                                   chatButton.config(command=continueDialogue)
                     if (comparison == SMALLER):
                            if (affectedNPC.getAffectionLevel() < amount):
                                   print(affectedNPC.getAffectionLevel())
                                   chatButton.config(command=continueDialogueToScene(altSceneIndex))
                            else:
                                   chatButton.config(command=continueDialogue)
              chatButton.pack(side="bottom")
       currentIndex:int = 0
       return updateDialogue()
picmain = "pic of main path"
picofJC = "pic of JC path"

def JC():
       window = Tk()
       window.title('SUTDoki')
       width = 1080
       height = 720 
       ws = window.winfo_screenwidth()
       hs = window.winfo_screenheight()
       x = (ws/2) - (width/2)
       y = (hs/2) - (height/2) - 100
       window.geometry('%dx%d+%d+%d' % (width, height, x, y))

       startingFrame = Frame(window)
       startingFrame.pack(anchor=W, fill=Y, expand=False, side=LEFT)
       Label(startingFrame, text="Enter your name").pack()
       nameInput = Entry(startingFrame)
       nameInput.pack()
       def txtImgOptNameSndAff(text:str, imgFilePath: str, options: list = [], name:str = None, soundFilePath: str = None, affectionCheck: dict = None):
            return {"text": text, "imgFilePath": imgFilePath, "name": name, "soundFilePath": soundFilePath, "options": options, "affectionCheck": affectionCheck}
       # ****FUNCTION txtImgOptNameSndAff****

       # "text" is what the dialogue in the chatbox reads, leave it empty during multiple option scenes.

       # "imgFilePath" is the relative image file path to this file, a few examples are shown (ONE image for each scene, edit the characters onto the image, 1080x550 resolution)

       # "name" is the name of the character who is speaking, it will appear in the name box at the top left of the chatbox, leave it empty to not have the name box shown.

       # "soundFilePath" is the relative sound file path to this file, a few examples are shown.

       # "affectionCheck" is a dictionary in this format {"NPC": XIAOMING, "comparison": SMALLER, "amount": 5, "altSceneIndex": 2 }. 
       # "NPC" is the NPC you want to check the affection level of.
       # "comparison" is to check whether it is smaller or bigger than the "amount".
       # "altSceneIndex" is the alternate scene you want to go to when the comparison returns TRUE.

       # "options" is a list that dictates what scenes the buttons go to.
       # If you have multiple options, create a list of dictionary
       # [{"text": "Scene 6", "nextSceneIndex": 6, "affection": {"affectedNPC": XIAOMING, "change": INCREASE}}, 
       #  {"text": "Scene 7", "nextSceneIndex": 7, "affection": {"affectedNPC": XIAOMING, "change": DECREASE}}] < like this
       # where "text" is the text shown in the option button, and "nextSceneIndex" is the scene's index in the array it will jump to when the button is pressed.
       # If you put options as a single number in a list e.g. [3], it will go to the scene at array index 3.
       # If you put options as [], an empty list, it will go to the scene in the next index.
       # "affection" is a dictionary that takes in the affected NPC and whether the button will INCREASE or DECREASE his affection.
       # If neutral, just put {"text": "Neutral Option Example", "nextSceneIndex": 8}, without "affection"
       # [{"text": "Positive Option Example", "nextSceneIndex": 6, "affection": {"affectedNPC": XIAOMING, "change": INCREASE}}, 
       #  {"text": "Negative Option Example", "nextSceneIndex": 7, "affection": {"affectedNPC": XIAOMING, "change": DECREASE}},
       #  {"text": "Neutral Option Example", "nextSceneIndex": 8} ] < like this

       # https://acedio.github.io/animalese.js/ < please use this to generate more animal crossing sounds, need to format this to .wav even though it is already .wav if not winsound wouldn't run it
       # https://cloudconvert.com/wav-converter < use this to reformat the animal crossing sounds
       
       textbox = Label(startingFrame, text="Starting Screen", borderwidth=2, background="#d1aa73", foreground="black", font="roboto")
       textbox.pack(side=LEFT)
       print (nameInput.get())
       # If not sure can check main for Finn examples
       # How to find out what index your dialogue is in the array: Take the current line of your array and subtract from the starting line. P.S: Put your dialogues in this vertical manner. 
       startButton = Button(startingFrame, text="Start Story", borderwidth=2, background="#d1aa73", foreground="black", font="roboto", command=lambda: 
              [protagonist.setName(nameInput.get()), (createScenes(window, startingFrame, 
              [txtImgOptNameSndAff("Day 1", "pictures/dog.png", [1]), 
              txtImgOptNameSndAff("Haiz, why does uni have to be so hard. Why can't the proffessor just give everyone passes", picmain, [2], nameInput.get(), "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are heading back dorm, you smelt an amazing scent coming from the kitchen)", picmain, [3]),
              txtImgOptNameSndAff("(Curiosity got the better of you as you decide to check it out.)", picmain, [4]),
              txtImgOptNameSndAff("(This seems to be some short of event happenning in the common kitchen)", "picture of kitchen", [5]),
              txtImgOptNameSndAff("(Thinking about it now, aren't the grub club in charge of the dessert aspect of the Prom.)", picmain, [6]),
              txtImgOptNameSndAff("Maybe I can sneak a peek at what dessert will be at prom in advanced!!", picmain, [7], nameInput.get(), "sounds/animalese (1).wav"), 
              txtImgOptNameSndAff("(As you are trying to see through the crowd to see what food they are preparing, a shadow can be seen creeping up behind her)", "pic of main with shadow", [8], "scary sound?"),
              txtImgOptNameSndAff("Oi!! What are you doing ?!?", "pic of shadow figure", [9], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(Wah!! Shit scared the hell outta me.)", picmain, [10], "scary sound?"),
              txtImgOptNameSndAff("(Who is the annoying guy spoiling my business!!!)", picmain, [11]),
              txtImgOptNameSndAff("(You turn around to see a tall handsome man with curly hair)", picofJC, [12], "wow sounds??"),
              txtImgOptNameSndAff("(OMG itss JungCook!!!)", picmain, [13]),
              txtImgOptNameSndAff("(You might be wondering why the Grub Club was in charge of the dessert for Prom)", [14]),
              txtImgOptNameSndAff("(It is all because of this one man! JungCook is from a renowned family of chef, he also has an impressive history of winning multiple competitions. He is the star chef of SUTD)", picofJC, [15]),
              txtImgOptNameSndAff("(JungCook has specially requested to help with the Prom dessert, with his reputation, no one would refuse his proposition!)", picofJC, [16]),
              txtImgOptNameSndAff("Hellooo, did you not hear me. WHAT ARE YOU DOING HERE!!!", picofJC, [17], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("", picofsun, [{"text": "Act SUS", "nextSceneIndex": 19, "affection": {"affectedNPC": JUNGCOOK, "change": INCREASE}}, {"text": "Ignore him", "nextSceneIndex": 24}, {"text": "Act Curious", "nextSceneIndex": 26, "affection": {"affectedNPC": JUNGCOOK, "change": DECREASE}}]),
              txtImgOptNameSndAff("O nothing im just here chilling randomly outside a window, for no apparent reason, just ignore me. ", picmain, [20], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Okay weirdo, give me a reason why I shouldn’t just report you for suspicious activity huh.", picofJC, [21], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Because of that UFO over there", picmain, [22], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As JungCook turns around, you immediately ran away.)", picmain, [23]),
              txtImgOptNameSndAff("What the!?? What a interesting lady she is.", picofJC, [28], "sound"),
              txtImgOptNameSndAff("(You stare at JungCook for awhile before turning and walking away)", picmain, [25]),
              txtImgOptNameSndAff("????????", picofJC, [28]),
              txtImgOptNameSndAff("O i'm just curious about what they are cooking ", picmain, [27], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("If you are curious about cooking, how about you pay attention to our grub club telegram rather than stand outside like a weirdo", picofJC, [28], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("WTF?!!??", picmain, [28], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Day End", picofmoon, [29]),
              txtImgOptNameSndAff("Day 2 ", picofsun, [30]),
              txtImgOptNameSndAff("(You just finished the last lesson of the day and is walking with your friend)", [31]),
              txtImgOptNameSndAff("Ahhh im stravinggg, wanna go eat gom-gom, canteen getting kinda boring", picmain, [32], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Sorry sis, i got project meeting right now. Have fun, CHAO!", "shadow human pic", [33], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Everyday project, haiz guess im going gom-gom alone", picmain, [34], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(Reaches Gom-Gom)", "pic of gomngom", [35]),
              txtImgOptNameSndAff("Didn’t expect gom-gom to have such a long queue today.", picmain, [35], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are queuing you hear a male voice behind you talking loudly, you turn around to realise that it was JungCook and as you saw him, he saw you as well)", [36]),
              txtImgOptNameSndAff("Huh didn’t expect to see you here again suspicious woman", picofJC, [37], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Nice to see you too!! Why can't you just say hello like normal people", picmain, [38], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("And just to clarify I wasn’t being weird I just happen to be there when you arrive ", picmain, [39], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Whatever", picofJC, [40], "sound"),
              txtImgOptNameSndAff("O what a sweet couple, we happen to have a promotion where you can get 2 sandwiches for 50%% off would you two like to share this?", picofshadow, [41], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("", picofsun, [{"text": "I will TAKE TWO FOR MYSELF", "nextSceneIndex": 42, "affection": {"affectedNPC": JUNGCOOK, "change": INCREASE}}, {"text": "No thanks", "nextSceneIndex": 46}, {"text": "Clarify the relationship", "nextSceneIndex": 55, "affection": {"affectedNPC": JUNGCOOK, "change": DECREASE}}]),
              txtImgOptNameSndAff("NOOO!!! I will take two chicken sandwichesss for myself, such a good offer", picmain, [43], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(JungCook rolling his eyes at your response)", picofJC, [44]),
              txtImgOptNameSndAff("I will just have a avocado bowl thanks", picofJC, [45], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are waitin for the food, JungCook starts having casual chat with you about school project as well as assignments, a friendship has started to form.)", [59]),
              txtImgOptNameSndAff("O no thanks, I will just have a chicken sandwich that’s all", picmain, [47], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Give me on avocado bowl thanks", picofJC, [48], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are waiting for the food to be prepared)", [49]),
              txtImgOptNameSndAff("You know you couldve ordered 2 chicken sandwich and split it with me, I wouldn’t have mind", picofJC, [50], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("I didn’t want to them to get the wrong idea that we are dating, we just met recently afterall. ", picmain, [51], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("We could be friends tho since we happened to meet coincidentally again so soon.", picmain, [52], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Sure im JungCook im sure you already know who I am", picofJC, [53], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Ahha I do know you, im {}, Nice to know you.".format(nameInput.get()), picmain, [54], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(After chatting while waiting for food, you left after taking your order. A new friendship was form)", [59]),
              txtImgOptNameSndAff("O no no no we aren't dating, he is just a random guy I met yesterday", picmain, [56], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("As If my standards would be so low, I rather date a cow then her.", picofJC, [57], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Heyyyyy!!! Rude much", picmain, [58], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You ordered a chicken sandwich and left after receiving it, you did not bother interacting with JungCook in anyway)", [59]),
              txtImgOptNameSndAff("Day End", picofmoon, [60]),
              txtImgOptNameSndAff("Day 3", picfsun, [70], "sound"),
              txtImgOptNameSndAff("(After lesson, you decided that studying in dorm was unproductive hence you decided to visit the library)",[71]),
              txtImgOptNameSndAff("Woah the library is surprisingly full today", picmain, [72], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are trying to find a seat, you spotted JungCook sitting alone in a corner, you also saw your group of friends sitting at the other side)", picmain, [73]),
              txtImgOptNameSndAff("(You decided to approach JungCook)", [74]),
              txtImgOptNameSndAff("Hi JC, I see you are reading a recipe book, is it so you can prepare me dinner?? ", picmain, [75], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("very funny. As you know im in charge of the dessert portion of the prom, I need to find a good dessert option for the day, something easy yet delicious. ", picofJC, [76], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Haiz, here I thought you would be treating your dear friend to your cooking.", pic, [77], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("One day one day I will cook for you.", picofJC, [78], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Anyways JC seriously?? Is that suppose to be my name?", picofJC, [79], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Ya, JungCook short form would be JC, such a good nickname", picmain, [80], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("", picofsun, [{"text": "Join JungCook to study", "nextSceneIndex": 81, "affection": {"affectedNPC": JUNGCOOK, "change": INCREASE}}, {"text": "Join your classmate ", "nextSceneIndex": 86}, {"text": "Joke with him", "nextSceneIndex": 89, "affection": {"affectedNPC": JUNGCOOK, "change": DECREASE}}]),
              txtImgOptNameSndAff("ANYWAYS NO GOING BACK ON YOUR WORDS, THAT WAS A PROMISE TO COOK ME A MEAL", picmain, [82], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Anyways mind if I sit here.", picmain, [83], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Nope", picofJC, [84], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You proceeded to study, as time pass you and JC had more conversation throughout the sessions until you have to leave for your project meeting)", [85]),
              txtImgOptNameSndAff("See you soon JC, I will wait for your treat", picmain, [93], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Ok see you next time then, imma go study with my classmate", picmain, [87], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Ok see you", picofJC, [88], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You study with your friends until you had to leave)", [93]),
              txtImgOptNameSndAff("Anyways, you should stop reading more recipe, you seem rounder today", picmain, [90], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Excuse me! I dare you to say that again.", picofJC, [91], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Jeez i'm just kidding, why gotta be so defensive", picmain, [92], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You then go to study with your friend)", picmain, [93], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Day End", picofmoon, [94]),
              txtImgOptNameSndAff("Day 4", picofsun, [95]),
              txtImgOptNameSndAff("God dammit why is this assignment so hard!!", picmain, [96], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(Looking at your phone you realise that you has been studying for 8 hours straight and that it is now 3am)", picmain, [97]),
              txtImgOptNameSndAff("I need to sleep if not I will miss tomorrow classes.", picmain, [98], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are standing up, you suddenly hear a rumbling noise from your stomach.)", picmain, [99]),
              txtImgOptNameSndAff("Hmm I guess I will go to the pantry and get a snack.", picmain, [100], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You proceeded to the pantry)", [101]),
              txtImgOptNameSndAff("Hmm what snack should I pick???", picmain, [102], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("You shouldn’t eat snack so late at night you know, it's bad for your health.", picshadow, [103], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("O god, O is just you JC, scared the hell outta me", picmain, [104], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("I have no choice man, I'm hungry and there isn’t anything for me to eat. If it's so unhealthy, why are you here as well", picmain, [105], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Please, does it look like I need to buy snacks? I'm the best chef here, when I'm hungry I can just cook myself a delicacy.", picofJC, [106], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Which is why I'm here, I'm was planning to cook a simple meal before I sleep.", picofJC, [107], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("", picofsun, [{"text": "Doubt Him", "nextSceneIndex": 108, "affection": {"affectedNPC": JUNGCOOK, "change": INCREASE}}, {"text": "Agree with him", "nextSceneIndex": 125}, {"text": "Cooking is EZ", "nextSceneIndex": 133, "affection": {"affectedNPC": JUNGCOOK, "change": DECREASE}}]),
              txtImgOptNameSndAff("Huhh best chef, when did you get that title, I don’t believe you. Unlesssss I get to taste the food you cook.", picmain, [109], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Tsk I don’t need your approval however my title and honour as the best chef In SUTD will not tolerate any insults. ", picofJC, [110], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Prepared to be blown away, food will never taste the same again.", picofJC, [111], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Ya right, prove me wrong", picmain, [112], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(Hehe free food from the chef JungCook himself WORTHHH!!!!)", picmain, [113]),
              txtImgOptNameSndAff("(JC was indeed an amazing chef, with his fast movement and precision knife work, he was able to make ingredients the way he wanted it.)", [114]),
              txtImgOptNameSndAff("(It looks so simple yet complex at the same time. Looking at him work, it was like watching a performance)", [115]),
              txtImgOptNameSndAff("(This didn’t last long as JC quickly prepared a simple dish of egg fried rice)", [116]),
              txtImgOptNameSndAff("Wow that was fast!", picmain, [117], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Of Course, a good chef does not keep his customers hungry", picofJC, [118], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Now for the main judging", picmain, [119], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("O wow, this is delicious.", picmain, [120], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("I mean hmm its acceptable, better than most fried rice I've tasted ", picmain, [121], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Don’t try to deny it, your action has already betrayed your words.", picofJC, [122], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("You can eat it slowly, I cooked more than one persons worth. Enjoy!!", picofJC, [123], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Thadwadnkss", picmain, [124], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You enjoyed yourself and thanked JC, you went to sleep)", [137]),
              txtImgOptNameSndAff("Well good for you that you know how to cook, I’ve never had any chance or time to learn cooking. ", picmain, [126], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Maybe one day I will ask you to teach me how to cook.", picmain, [127], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("No problem, just hit me up and I will teach you the best cooking tutorial you have ever seen", picofJC, [128], "sound"),
              txtImgOptNameSndAff("Anyways what are you cooking?", picmain, [129], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Just a simple egg fried rice, do you want some as well?", picofJC, [130], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("If you wouldn’t mind cooking extra, I would love to have your cooking.", picmain, [131], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(JC nods and proceed to cook fried rice)", [132]),
              txtImgOptNameSndAff("(You eat the fried rice with pleasure and awe, you then leave after finishing and saying goodbye)", [137]),
              txtImgOptNameSndAff("Show off! You can cook so what, I don’t think cooking is that hard anyway.", picmain, [134], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Its certainly harder than you just yapping, get out of my way, I need to get my equipments.", picofJC, [135], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("TSK this pantry aint yours.", picmain, [136], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You bought snacks and leave)", [137]),
              txtImgOptNameSndAff("Day End", picofmoon, [138]),
              txtImgOptNameSndAff("Day 5", picofsun, [139], "sound"),
              txtImgOptNameSndAff("(Today was a chill day, you enjoyed the peaceful moments (Affection with JungCook too low))", picmain, ['day end no'], {"NPC": JUNGCOOK, "comparison": BIGGER, "amount": 3, "altSceneIndex": 140 }),
              txtImgOptNameSndAff("(You just finished her fifth row of volleyball training)", [141]),
              txtImgOptNameSndAff("Good training guys, see you guys CHAOOO", picmain, [142], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Woo, all those workout got me famished, what do I want what do I want", picmain, [143], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Hmm Mcd sounds good, hmm meggi sounds amazing as well. O man how I wish I could just get both.", picmain, [144], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(As you are thinking about what to eat, JungCook approaches you)", [145]),
              txtImgOptNameSndAff("O hi, JC.", picmain, [146], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Yo, you free now? ", picofJC, [147], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("YASss, why?", picmain, [148], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Nothing much just that remember when I owe you dinner, well I’m free now to cook for you", picofJC, [149], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("", picofsun, [{"text": "LETSS GOOOOO", "nextSceneIndex": 150, "affection": {"affectedNPC": JUNGCOOK, "change": INCREASE}}, {"text": "Be Polite", "nextSceneIndex": 155}, {"text": "Reject Him", "nextSceneIndex": 159, "affection": {"affectedNPC": JUNGCOOK, "change": DECREASE}}]),
              txtImgOptNameSndAff("Letss gooooooo, I was just nice hungry after training. I will say first, I not someone with a small stomach.", picmain, [151], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("No problem, do you know who I am? My name is Cook, JungCook.", picofJC, [152], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Cooking a meal for the whole school wouldn’t be an issue to me much less one person.", picofJC, [153], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Hahha good, I shall feast tonight then.", picmain, [154], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You followed JC to the block communal kitchen where JC had prepared the food ingredients beforehand. JC cooked a feast for you and you two enjoyed yourselves)", [164]),
              txtImgOptNameSndAff("Oo, I was just joking hahah, I wont force you to treat me dinner.", picmain, [156], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("No issue, I have already prepared the ingredients in advanced. You can think of it as me treating my friend to dinner. I am your friend right?", picofJC, [157], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Of Course, well lets go then. Thank you for the meal.", picmain, [158], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("(You followed JC to the block communal kitchen where JC had prepared the food ingredients beforehand. JC cooked a feast for you and you two enjoyed yourselves)", [164]),
              txtImgOptNameSndAff("Thanks but no thanks, imma go mac.", picmain, [160], "sounds/animalese (1).wav"),
              txtImgOptNameSndAff("Actually picking mcd over my cooking? Tsk suit urself.", picofJC, [161]), 
              txtImgOptNameSndAff("(JungCook walk away)", [162]), 
              txtImgOptNameSndAff("Eh whatever", picmain, [163], "sounds/animalese (1).wav"), 
              txtImgOptNameSndAff("(You ordered mac delivery and enjoyed yourself)", [164]), 
              txtImgOptNameSndAff("Day End", picofmoon, [165]), 
              txtImgOptNameSndAff("Day 6", picofsun, [166]), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'),  
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 
              txtImgOptNameSndAff("", pic, [], 'sound'), 




              ]))])
       startButton.pack(side=RIGHT)
       window.mainloop()
     