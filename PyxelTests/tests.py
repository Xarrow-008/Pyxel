
c1 = True
c2 = False
c3 = True
c4 = False

'''
def lampe(x,y,t_depart):
    i = 0

    return [x,y,i]




tab= [c1 and c3,[c3,False],[c4,True]]

def test_boolean_in_tab(tab):
    global c3
    if tab[0]:
        print('YASSSSS ANNNDDD')
        tab[1][0] = tab[1][1]
    print(c3)
    print(tab)

test_boolean_in_tab(tab)
print(c3)




SLASH = [0,0,False]
def consequence():
    boom = True
    return boom

tableau = [[c1 and (c2 or c3),[[SLASH,2,True],[SLASH,3,False]],10]]
frame= 25


def easy_frames_event(tab,timeEvent):
    global frame
    for event in tab:
        if event[0] and frame - timeEvent < event[2]:
            event[1][0][event[1]] = event[1][1]

easy_frames_event(tableau,20)

print(SLASH)
'''

book1 = {'x':0}
book2 = {'x':1}
book3 = {'x':2}

shelf = [book1,book2,book3]

for book in shelf:
    if book['x'] == 0:
        shelf.remove(book)

print(shelf)
