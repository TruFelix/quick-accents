import keyboard

isHoldingShift = False
isHoldingSpace  = False
# shiftCode differentiates between left and right
# shiftCode = 42 # yes really, I didn't make this code up so shut up
spaceCode = 57

holdingCharacter=None

alphabet = ['a','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


def updateShiftState(event: keyboard.KeyboardEvent):
    global isHoldingShift

    isDownEvent = event.event_type == keyboard.KEY_DOWN
    isUpEvent = event.event_type == keyboard.KEY_UP

    if isDownEvent:
        if event.name == 'shift':
            isHoldingShift = True
    
    if isUpEvent:
        if event.name == 'shift':
            isHoldingShift = False

def updateSpaceState(event: keyboard.KeyboardEvent):
    global isHoldingSpace

    isDownEvent = event.event_type == keyboard.KEY_DOWN
    isUpEvent = event.event_type == keyboard.KEY_UP

    if isDownEvent:
        if event.scan_code == spaceCode:
            isHoldingSpace = True
    
    if isUpEvent:
        if event.scan_code == spaceCode:
            isHoldingSpace = False

def updateHoldingCharacterState(event: keyboard.KeyboardEvent):
    global holdingCharacter

    isDownEvent = event.event_type == keyboard.KEY_DOWN
    isUpEvent = event.event_type == keyboard.KEY_UP

    if isDownEvent:
        if event.name in alphabet:
            holdingCharacter = event.name
    
    if isUpEvent:
        if holdingCharacter is None or event.name == holdingCharacter:
            holdingCharacter = None

def log(event: keyboard.KeyboardEvent):
    if event.event_type == keyboard.KEY_DOWN:
        print(f"{event.name} = {event.scan_code} | down", end="")

    if event.event_type == keyboard.KEY_UP:
        print(f"{event.name} = {event.scan_code} | up", end="")
    
    print(f" | holding: {'shift + ' if isHoldingShift else ''} {holdingCharacter if holdingCharacter is not None else 'XXXX'} {' + SPACE' if isHoldingSpace else ''}")

def mapEventFromTo(event: keyboard.KeyboardEvent, f:str, t:str):
    global holdingCharacter, isHoldingCharacter, isHoldingShift

    shouldBeUppercase = f.isupper()
    shiftRequired = shouldBeUppercase
    replaceAsHotkey = len(t) > 1

    # print(f"'{f}' {'is' if shouldBeUppercase else 'is not'} uppercase: replace with '{t}'")

    if holdingCharacter == f.lower() and isHoldingSpace:
        if (shiftRequired and isHoldingShift) or not shiftRequired:
            print(f"hit! replace with '{t}'")
            # hit! we should now convert:
            keyboard.send("backspace") # one for the 'character'
            keyboard.send("backspace") # one for the 'space'
            
            # release all keys, because otherwise it can conflict with the write command
            # as that also uses only a keycombination to write the chars
            keyboard.release("shift")
            keyboard.release("space")
            keyboard.release(event.name)
            keyboard.restore_modifiers([])
            
            if replaceAsHotkey:
                steps = t.split(',')
                for step in steps:
                    keyboard.send(step)
                keyboard.send(steps[-1])
            else:
                keyboard.write(t, exact=True, restore_state_after=False)
            return True

while True:
    # wait for a base character
    event = keyboard.read_event(suppress=True)

    updateShiftState(event)
    updateSpaceState(event)
    updateHoldingCharacterState(event)

    # logging as you wish, for debugging?
    # log(event)

    isDownEvent = event.event_type == keyboard.KEY_DOWN
    isUpEvent = event.event_type == keyboard.KEY_UP

    isHoldingCharacter = holdingCharacter is not None

    hit = False
    hit = hit or mapEventFromTo(event, "A", "Ä")
    hit = hit or mapEventFromTo(event, "O", "Ö")
    hit = hit or mapEventFromTo(event, "U", "alt gr,shift+',shift+u")
    hit = hit or mapEventFromTo(event, "s", "ß")
    hit = hit or mapEventFromTo(event, "a", "ä")
    hit = hit or mapEventFromTo(event, "o", "ö")
    hit = hit or mapEventFromTo(event, "u", "alt gr,shift+',u")

    # cleanup
    if hit:
        isHoldingSpace = False
        isHoldingCharacter = False
        