import pyxel, os, random, math

WIDTH = 128

LETTERS = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
PONCTUATION = " ,;:!’(-)"
PONC_SHIFT = " ?./§456°"
PONC_ALT = "    {[|]"
PONC_PYXEL = ['SPACE','COMMA','SEMICOLON','COLON','EXCLAIM','4','6']
KEYS = LETTERS+PONCTUATION

OBPA = ["Tu me fends l’âme. Quoi ! pas un souvenir, Camille ? Pas un battement de cœur pour notre enfance, pour tout ce pauvre temps passé, si bon, si doux, si plein de niaiseries délicieuses ? Tu ne veux pas venir voir le sentier par où nous allions à la ferme ?",
        "Je veux aimer, mais je ne veux pas souffrir ; je veux aimer d’un amour éternel, et faire des serments qui ne se violent pas. Voilà mon amant.",
        "Tous les hommes sont menteurs, inconstants, faux, bavards, hypocrites, orgueilleux ou lâches, méprisables et sensuels; toutes les femmes sont perfides, artificieuses, vaniteuses, curieuses et dépravées ; le monde n’est qu’un égout sans fond où les phoques les plus informes rampent et se tordent sur des montagnes de fange ; mais il y a au monde une chose sainte et sublime, c’est l’union de deux de ces êtres si imparfaits et si affreux.",
        "J’ai souffert souvent, je me suis trompé quelquefois ; mais j’ai aimé. C’est moi qui ai vécu, et non pas un être factice créé par mon orgueil et mon ennui.",
        "Si je vous épousais, ne devriez-vous pas répondre avec franchise à toutes mes questions, et me montrer votre cœur à nu ?",
        "Elles qui te représentent l’amour des hommes comme un mensonge, savent-elles qu’il y a pis encore, le mensonge de l’amour divin?",
        "Y croyez-vous, vous qui parlez? Vous voilà courbé près de moi avec des genoux qui se sont usés sur les tapis de vos maîtresses, et vous n’en savez plus le nom.",
        "Non, non, Camille, je ne t’aime pas ; je ne suis pas au désespoir. Je n’ai pas le poignard dans le cœur et je te le prouverai. Oui, tu sauras que j’en aime une autre avant que de partir d’ici.",
        "Tu ne sais pas lire ; mais tu sais ce que disent ces bois et ces prairies, ces tièdes rivières, ces beaux champs couverts de moissons, toute cette nature splendide de jeunesse. Tu reconnais tous ces milliers de frères, et moi pour l’un d’entre eux ; lève-toi ; tu seras ma femme, et nous prendrons racine ensemble dans la sève du monde tout-puissant.",
        "Hélas ! monsieur le docteur, je vous aimerai comme je pourrai.",
        "Je t’aime, Camille, voilà tout ce que je sais.",
        "Je ne vous aime pas, moi : je n’ai pas été chercher par dépit cette malheureuse enfant au fond de sa chaumière, pour en faire un appât, un jouet.",
        "Pauvre innocente ! [...] Il t’a fait de beaux discours, n’est-ce pas? Gageons qu’il t’a promis de t’épouser.",
        "Tu l’aimes, pauvre fille ; il ne t’épousera pas, et la preuve, je vais te la donner.",
        "Connaissez-vous le cœur des femmes, Perdican ? Êtes-vous sûr de leur inconstance, et savez-vous si elles changent réellement de pensée en changeant de langage? [...] Sans doute, il nous faut souvent jouer un rôle, souvent mentir ; vous voyez que je suis franche ; mais êtes-vous sûr que tout mente dans une femme, lorsque sa langue ment ?",
        "Est-ce qu’il l’épouserait tout de bon ? [...] Mais qu’est-ce donc que tout cela? Je n’en puis plus, mes pieds refusent de me soutenir."]



class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(WIDTH,WIDTH,title='MonkeyType',fps = 60)

        self.text = Text(OBPA[0])
        self.current_key = ''

        pyxel.run(self.update,self.draw)

    def update(self):
        self.current_key = ''
        for letter in LETTERS:
            if pyxel.btnp(getattr(pyxel,'KEY_'+letter)):
                self.current_key = letter

        for i in range(len(PONC_PYXEL)):
            if pyxel.btnp(getattr(pyxel,'KEY_'+PONC_PYXEL[i])):
                if pyxel.btn(pyxel.KEY_SHIFT):
                    self.current_key = PONC_SHIFT[i]
                elif pyxel.btn(pyxel.KEY_RALT):
                    self.current_key = PONC_ALT[i]
                    print(PONC_ALT[i],flush=True)
                else:
                    self.current_key = PONCTUATION[i]
                
        if self.current_key != '':
            self.text.update(self.current_key)
            if self.text.completed:
                self.text.__init__()
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,self.text.typed,9)
        pyxel.text(10+4*self.text.pos,10,self.text.remaining,7)

class Text:
    def __init__(self,txt):
        self.text = txt
        self.pos = 0
        self.remaining = self.text
        self.typed = ''
        self.completed = False
        pyxel.camera(0,0)
        self.margin = 2.5    
    def update(self,key):
        if not self.completed:
            if key == self.text[self.pos].upper():
                self.pos += 1
                if self.pos == len(self.text):
                    self.completed = True
            
            self.typed = ''
            self.remaining = ''
            for i in range(len(self.text)):
                if i < self.pos:
                    self.typed += self.text[i]
                else:
                    self.remaining += self.text[i]
        
        self.getCam()
        
    def getCam(self):
        x = 4*self.pos + 10
        if x >= WIDTH//self.margin:
            pyxel.camera(x-WIDTH//self.margin,0)

def getIndex(tab,value):
    for i in range(len(tab)-1):
        if tab[i] == value:
            return i


App()