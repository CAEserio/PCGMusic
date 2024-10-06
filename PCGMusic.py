from midiutil.MidiFile import MIDIFile
import pygame
import os
import random
midiNotes = {
    'C':61,'C#':62,'D':63,'D#':64,
    'E':65,'F':66,'F#':67,'G':68,
    'G#':69, 'A':70,'A#':71,'B':72
}

notes = ['C','C#','D','D#',
         'E','F','F#','G',
         'G#','A','A#','B',]




def random_seed(length):
    random.seed()
    min = 10**(length-1)
    max = 9*min + (min-1)
    return random.randint(min, max)

def selectKey(seed,pattern):
    keyPatternMajor = [2,2,1,2,2,2,1]
    keyPatternMinor =  [2, 1, 2, 2, 1, 2, 2]
    match pattern:
        case "major":
            keyPattern = keyPatternMajor
        case "minor":
            keyPattern = keyPatternMinor
    selectedKeySig = []
    midiKeySig = []
    print( "Your Random Generated Seed is " + seed) 
    #selectedKey = input()
    selectedIndex = int(random.choice(seed))
    selectedKeySig.append(notes[selectedIndex])

    for i in keyPattern:
        indexToAppend = (selectedIndex + i) % 12
        selectedKeySig.append(notes[indexToAppend])
        selectedIndex = indexToAppend
    print(selectedKeySig)
    for note in selectedKeySig:
        midiKeySig.append(midiNotes[note])
    print(midiKeySig)
    for value in range(len(midiKeySig)):
        pass
        #midiKeySig.append(midiKeySig[value] - 12)
        #midiKeySig.append(midiKeySig[value] + 12)
        #midiKeySig.append(midiKeySig[value] + 24)
        #midiKeySig.append(midiKeySig[value] -24)
    return midiKeySig

def selectTempo():
    print("What should this music be for?")
    print("Overworld, Dungeon(exploration), Main Theme, Dungeon(combat), Overworld (Combat)")
    selection = input()
    key = ""
    match selection.lower():
        case "overworld":
            randomTempo = random.randint(120,140)
            key = "major"
        case "dungeon(exploration)":
            randomTempo = random.randint(70,80)
            key = "minor"
        case "dungeon(combat)":
            randomTempo = random.randint(200,360)
            key = "minor"
        case "main theme":
            randomTempo = random.randint(100,130)
            key = "major"
        case "overworld(combat)":
            randomTempo = random.randint(200,360)
            key = "major"
    return randomTempo,key


def randomMelody(selectedMidiKey):
    mf = MIDIFile(2)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time,180)
    channel = 0
    volume = 100
    generatedMelody = []
    selectedMidiKey.append("REST")
    #melody = stream.Stream()
   
    
    #isItFit = melodyRules(melody)
    #Returns True or False

    for i in range(100):
        noteChoice = random.choice(selectedMidiKey)
        if noteChoice != "REST":
            #mf.addNote(track, channel, noteChoice, i, 1, volume)
            generatedMelody.append(noteChoice)
        else:
            pass
            generatedMelody.append("REST")
    
    return generatedMelody

def mutate(generatedMelody,selectedMidiKey):
    mutationRate = 5
    for i in range(len(generatedMelody)):
        mutation = random.randint(0,10)
        if (mutation  < mutationRate):
            generatedMelody[i] = random.choice(selectedMidiKey)
    return generatedMelody
    
def printToScore(melody,selectedMidiKey,num,selectedTempo):
    mf = MIDIFile(2)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, selectedTempo)
    channel = 0
    volume = 100

    mf.addNote(1,channel,selectedMidiKey[1],0,4,int(volume/2))
    mf.addNote(1,channel,selectedMidiKey[0 + 3],0,4,int(volume/2))
    mf.addNote(1,channel,selectedMidiKey[0 + 3 + 3],0,4,int(volume/2))
    for i in range(len(melody)):
        if (melody[i] != "REST"):
            mf.addNote(track,channel,melody[i],i,1,volume)
    
    for i in range(4,100,4):
        chordChoice = random.randint(1,6)
        mf.addNote(1,channel,selectedMidiKey[chordChoice],i,4,int(volume/2))
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3) %8],i,4,int(volume/2))
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3 +3) %8],i,4,int(volume/2))
    mf.addNote(1,channel,selectedMidiKey[0],100,4,int(volume/2))
    mf.addNote(1,channel,selectedMidiKey[0 + 3],100,4,int(volume/2))
    mf.addNote(1,channel,selectedMidiKey[(0 + 3 + 3) % 8],100,4,int(volume/2))
    with open("outputTEST"+str(num)+".mid", 'wb') as outf:
        mf.writeFile(outf)
            
def melodyRules(melody,notes,add):
    score = 0

    #Tonic - First and Last Notes of the Scale. Melody revolves around the proper use of the tonic
    #Correct Finish to the Tonic
    for i in range(1, len(melody)):
     if melody[i - 1] == notes[-2] and melody[i] == notes[0]:
        score += 1

    #Stepwise Motion- Interval Between two consecutive pitch should be no more than a step
    for i in range(1, len(melody)):
        try:
            interval = abs(melody[i] - melody[i - 1])
        except:
            interval = 0
        if interval == 1:
            score += 1

    #Melodic Contour: Checks if there are large jumps betwen notes. Large Jumps are penalized
    for i in range(1, len(melody)):
        try:
            interval = abs(melody[i] - melody[i - 1])
        except:
            interval = 0
        if interval > 4 and interval != 1:
            score -= 2  


    #Repeated Motifs: We check if the melody repeats short patterns of 3 notes. Repeating motifs are awarded
    motif_counts = {}
    for i in range(1, len(melody) - 2):
        motif = melody[i:i + 3]
        motif_str = str(motif)
        if motif_str in motif_counts:
            motif_counts[motif_str] += 1
        else:
            motif_counts[motif_str] = 1

    repeated_motif_count = sum(count for count in motif_counts.values() if count > 1) 
    score += repeated_motif_count


    if melody[0] == notes[0]:
        score += 1
    if melody[-1] == notes[0]:
        score += 1
    #Reward the resolution from the 7th scale degree to the tonic
    for i in range(1, len(melody)):
        if melody[i - 1] == notes[-2] and melody[i] == notes[0]:
            score += 1

    if melody[0] == notes[0]:
        score += 20
    if melody[-1] == notes[0]:
        score += 20
    
    if score >= (4 * add):
        return  True
    else:
        return False

seed = str(random_seed(10))


tempo,pattern = selectTempo()
selec = selectKey(seed,pattern)

melody = randomMelody(selec)
while (not melodyRules(melody,selec,0)):
        mutate(melody,selec)
        print(melody)
printToScore(melody,selec,1,tempo)
clock = pygame.time.Clock()
melody2 = randomMelody(selec)
while (not melodyRules(melody2,selec,0)):
        mutate(melody2,selec)
        print(melody2)
printToScore(melody2,selec,2,tempo)

melody3 = randomMelody(selec)

while (not melodyRules(melody3,selec,0)):
        mutate(melody3,selec)
        print(melody3)
printToScore(melody3,selec,3,tempo)

melody4 = randomMelody(selec)


printToScore(melody4,selec,4,tempo)
melody5 = randomMelody(selec)

while (not melodyRules(melody4,selec,0)):
        mutate(melody4,selec)
        print(melody4)

printToScore(melody5,selec,5,tempo)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples

pygame.mixer.init(freq, bitsize, channels, buffer)
# pygame.mixer.music.load("outputTEST1.mid")
# pygame.mixer.music.play()
print("playing melody1")

while pygame.mixer.music.get_busy():
    clock.tick(30)

# pygame.mixer.music.load("outputTEST2.mid")
# pygame.mixer.music.play()
print("playing melody2")

while pygame.mixer.music.get_busy():
    clock.tick(30)
# 
# pygame.mixer.music.load("outputTEST3.mid")
# pygame.mixer.music.play()
print("playing melody3")

while pygame.mixer.music.get_busy():
    clock.tick(30)

# pygame.mixer.music.load("outputTEST4.mid")
# pygame.mixer.music.play()
print("playing melody4")

while pygame.mixer.music.get_busy():
    clock.tick(30)

# pygame.mixer.music.load("outputTEST5.mid")
# pygame.mixer.music.play()
print("playing melody5")

while pygame.mixer.music.get_busy():
    clock.tick(30)

print("Please input the number of the melody you like the best (melody1, melody2, melody3, melody4, melody5)")
melodicChoice = int(random.choice(seed))%5
if melodicChoice == 0:
    melodicChoice += 1
print(melodicChoice)
match melodicChoice:
    case 1:
        melodyToMutate = melody
    case 2:
        melodyToMutate = melody2
    case 3:
        melodyToMutate = melody3
    case 4:
        melodyToMutate = melody4
    case 5:
        melodyToMutate = melody5
melodicChoice = None
for i in range(3):
    mutation1 = mutate(melodyToMutate,selec)
    while (not melodyRules(mutation1,selec,i*5)):
        mutate(mutation1,selec)
        print(mutation1)
    printToScore(melody,selec,1,tempo)
    print(mutation1)
    printToScore(melody,selec,"mutation1" + "generation" + str(i+1),tempo)
    mutation2 = mutate(melodyToMutate,selec)
    while (not melodyRules(mutation2,selec,i)):
        mutate(mutation2,selec)
        print(mutation2)
    print(mutation2)
    printToScore(melody,selec,"mutation2"+ "generation" + str(i+1),tempo)
    mutation3 = mutate(melodyToMutate,selec)
    while (not melodyRules(mutation3,selec,i)):
        mutate(mutation3,selec)
        print(mutation3)
    print(mutation3)
    printToScore(melody,selec,"mutation3"+ "generation" + str(i+1),tempo)
    mutation4 = mutate(melodyToMutate,selec)
    while (not melodyRules(mutation4,selec,i)):
        mutate(mutation4,selec)
        print(mutation4)
    printToScore(melody,selec,"mutation4"+ "generation" + str(i+1),tempo)
    print(mutation4)
    mutation5 = mutate(melodyToMutate,selec)
    while (not melodyRules(mutation5,selec,i)):
        mutate(mutation5,selec)
        print(mutation5)
    print(mutation5)
    printToScore(melody,selec,"mutation5"+ "generation" + str(i+1),tempo)

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    # pygame.mixer.music.load("outputTESTmutation1"+ "generation" + str(i+1)+".mid")
    # pygame.mixer.music.play()
    print("playing mutated melody1")

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    # pygame.mixer.music.load("outputTESTmutation2"+ "generation" + str(i+1)+".mid")
    # pygame.mixer.music.play()
    print("playing mutated melody2")

    while pygame.mixer.music.get_busy():
        clock.tick(30)
    # pygame.mixer.music.load("outputTESTmutation3"+ "generation" + str(i+1)+".mid")
    # pygame.mixer.music.play()
    print("playing mutated melody3")

    while pygame.mixer.music.get_busy():
        clock.tick(30)
    # pygame.mixer.music.load("outputTESTmutation4"+ "generation" + str(i+1)+".mid")
    # pygame.mixer.music.play()
    print("playing mutated melody4")

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    # pygame.mixer.music.load("outputTESTmutation5"+ "generation" + str(i+1)+".mid")
    # pygame.mixer.music.play()
    print("playing mutated melody5")

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    print("Please input the number of the melody you like the best (melody1, melody2, melody3, melody4, melody5)")
    melodicChoice = int(random.choice(seed))%5
if melodicChoice == 0:
    melodicChoice += 1
    match melodicChoice:
        case 1:
            melodyToMutate = mutation1
        case 2:
            melodyToMutate = mutation2
        case 3:
            melodyToMutate = mutation3
        case 4:
            melodyToMutate = mutation4
        case 5:
            melodyToMutate = mutation5
print("your final melody chosen is" + str(melodyToMutate))
os.startfile("outputTESTmutation"+str(melodicChoice)+"generation3"+".mid")
#print(melody)
#mutate(melody,selec)
#print(melody)
