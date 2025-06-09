import pyxel, os, random, math

WIDTH = 128

LETTERS = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
PONCTUATION = " ,;:!'(-)"
PONC_SHIFT = " ?./§456°"
PONC_ALT = "     {[|]"
PONC_PYXEL = ['SPACE','COMMA','SEMICOLON','COLON','EXCLAIM','4','5','6','RIGHTPAREN']
KEYS = LETTERS+PONCTUATION

OBPA = ["Tu me fends l'ame. Quoi! pas un souvenir, Camille? Pas un battement de coeur pour notre enfance, pour tout ce pauvre temps passe, si bon, si doux, si plein de niaiseries delicieuses? Tu ne veux pas venir voir le sentier par ou nous allions a la ferme?",
        "Je veux aimer, mais je ne veux pas souffrir; je veux aimer d'un amour eternel, et faire des serments qui ne se violent pas. Voila mon amant.",
        "Tous les hommes sont menteurs, inconstants, faux, bavards, hypocrites, orgueilleux ou laches, meprisables et sensuels; toutes les femmes sont perfides, artificieuses, vaniteuses, curieuses et depravees; le monde n'est qu'un egout sans fond ou les phoques les plus informes rampent et se tordent sur des montagnes de fange; mais il y a au monde une chose sainte et sublime, c'est l'union de deux de ces etres si imparfaits et si affreux.",
        "J'ai souffert souvent, je me suis trompe quelquefois; mais j'ai aime. C'est moi qui ai vecu, et non pas un etre factice cree par mon orgueil et mon ennui.",
        "Si je vous epousais, ne devriez-vous pas repondre avec franchise a toutes mes questions, et me montrer votre coeur a nu?",
        "Elles qui te representent l'amour des hommes comme un mensonge, savent-elles qu'il y a pis encore, le mensonge de l'amour divin?",
        "Y croyez-vous, vous qui parlez? Vous voila courbe pres de moi avec des genoux qui se sont uses sur les tapis de vos maitresses, et vous n'en savez plus le nom.",
        "Non, non, Camille, je ne t'aime pas; je ne suis pas au desespoir. Je n'ai pas le poignard dans le coeur et je te le prouverai. Oui, tu sauras que j'en aime une autre avant que de partir d'ici.",
        "Tu ne sais pas lire; mais tu sais ce que disent ces bois et ces prairies, [...] leve-toi; tu seras ma femme.",
        "Helas! monsieur le docteur, je vous aimerai comme je pourrai.",
        "Je t'aime, Camille, voila tout ce que je sais.",
        "Je ne vous aime pas, moi: je n'ai pas ete chercher par depit cette malheureuse enfant au fond de sa chaumiere, pour en faire un appat, un jouet.",
        "Pauvre innocente! [...] Il t'a fait de beaux discours, n'est-ce pas? Gageons qu'il t'a promis de t'epouser.",
        "Tu l'aimes, pauvre fille; il ne t'epousera pas, et la preuve, je vais te la donner.",
        "Connaissez-vous le coeur des femmes, Perdican? etes-vous sur de leur inconstance, et savez-vous si elles changent reellement de pensee en changeant de langage? [...] Sans doute, il nous faut souvent jouer un role, souvent mentir; vous voyez que je suis franche; mais etes-vous sur que tout mente dans une femme, lorsque sa langue ment?",
        "Est-ce qu'il l'epouserait tout de bon? [...] Mais qu'est-ce donc que tout cela? Je n'en puis plus, mes pieds refusent de me soutenir."]



class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(WIDTH,WIDTH,title='MonkeyType',fps = 60)

        self.txtList = OBPA
        self.text = Text(self.txtList,0)
        self.current_key = ''
        self.pb_time = 848

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
                else:
                    self.current_key = PONCTUATION[i]
                
        if self.current_key != '':
            self.text.update(self.current_key)
        
            if self.text.completed:
                if self.text.index < len(self.txtList) - 1:
                    self.text.index += 1
                else:
                    self.text.index = 0
                    self.time = pyxel.frame_count//60

                self.text.__init__(self.txtList,self.text.index)
        
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,self.text.typed,9)
        pyxel.text(10+4*self.text.pos,10,self.text.remaining,7)
        pyxel.text(10+4*self.text.pos,13,'_',11)
        pyxel.text(10+self.text.camx,30,'Time: '+str(pyxel.frame_count//60),8)
        pyxel.text(10+self.text.camx,38,'Best Time: '+str(self.pb_time),14)

class Text:
    def __init__(self,txtList,index):
        self.text = txtList[index]
        self.pos = 0
        self.remaining = self.text
        self.typed = ''
        self.completed = False
        pyxel.camera(0,0)
        self.camx = 0
        self.margin = 2.5
        self.index = index

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
            self.camx = x-WIDTH//self.margin
            pyxel.camera(self.camx,0)

def getIndex(tab,value):
    for i in range(len(tab)-1):
        if tab[i] == value:
            return i


App()