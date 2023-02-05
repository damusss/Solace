import solace
from errors import ExitError

while True:
    text = input("solace> ")
    if not text.strip(): continue
    res,err = solace.run("<stdin>",text)
    
    if err:
        print(err.as_string())
        if isinstance(err,ExitError):
            break
    elif res: 
        if len(res.elements) == 1:
            print(repr(res.elements[0]))
        else:
            print(repr(res))