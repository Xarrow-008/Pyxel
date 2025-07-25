import pyxel, os, random, math

FPS = 20
WIDTH = 128

LETTERS = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
PONCTUATION = " ,;:!'(-)"
PONC_SHIFT = " ?./§456°"
PONC_ALT = "     {[|]"
PONC_PYXEL = ['SPACE','COMMA','SEMICOLON','COLON','EXCLAIM','4','5','6','RIGHTPAREN']
KEYS = LETTERS+PONCTUATION

OBPA = ["Tu me fends l'ame. Quoi! pas un souvenir, Camille? Pas un battement de coeur pour notre enfance?",
        "Je veux aimer, mais je ne veux pas souffrir",
        "Tous les hommes sont menteurs, inconstants, faux, bavards, hypocrites, orgueilleux ou laches, meprisables et sensuels; toutes les femmes sont perfides, artificieuses, vaniteuses, curieuses et depravees; le monde n'est qu'un egout sans fond ou les phoques les plus informes rampent et se tordent sur des montagnes de fange; mais il y a au monde une chose sainte et sublime, c'est l'union de deux de ces etres si imparfaits et si affreux",
        "J'ai souffert souvent, je me suis trompe quelquefois; mais j'ai aime. C'est moi qui ai vecu, et non pas un etre factice cree par mon orgueil et mon ennui.",
        "Non, non, Camille, je ne t'aime pas; je ne suis pas au desespoir. Je n'ai pas le poignard dans le coeur et je te le prouverai. Oui, tu sauras que j'en aime une autre avant que de partir d'ici",
        "Tu ne sais pas lire; mais tu sais ce que disent ces bois et ces prairies [...] leve-toi; tu seras ma femme",
        "Connaissez-vous le coeur des femmes, Perdican? etes-vous sur de leur inconstance, et savez-vous si elles changent reellement de pensee en changeant de langage? [...] etes-vous sur que tout mente dans une femme, lorsque sa langue ment?"]

DDFC = ["Homme, es-tu capable d'etre juste? [...] Dis-moi? Qui t'a donne le souverain empire d'opprimer mon sexe? Ta force? Tes talents?",
        "La Femme nait libre et demeure egale a l'homme en droits",
        "La femme a le droit de monter sur l'echafaud; elle doit avoir egalement celui de monter a la tribune",
        "Toute Citoyenne peut donc dire librement: Je suis mere d'un enfant qui vous appartient",
        "L'homme esclave a multiplie ses forces, a eu besoin de recourir aux tiennes pour briser ses fers",
        "Femme, reveille-toi; le tocsin de la raison se fait entendre dans tout l'univers; reconnais tes droits",
        "O femmes! Femmes, quand cesserez-vous d'etre aveugles? Quels sont les avantages que vous avez recueillis dans la revolution?",
        "Le mariage est le tombeau de la confiance et de l'amour"]

MOUVEMENTS = [  '16e: humanisme: redoedcouvre culte grecque et latine, rejette moyen age',
                '1547-1570: la playade: mouvement humanisme, enrichissent la langue francaise',
                "17e: le baroc: mouvement chaotique en opposition a l'humanisme",
                "17e: classisisme: retour a l'ordre - theatre 3 actes",
                "18e: les lumieres: philososophes progressifs ouvert aux sciences",
                "19e: romantisme: exaltation des sentiments"]

class App:
    def __init__(self):
        os.system('cls')
        pyxel.init(WIDTH,WIDTH//5*3,title='MonkeyType',fps = FPS)

        self.txtList = DDFC+OBPA
        self.text = Text(self.txtList,0)
        self.current_key = ''
        self.pb_time = 718
        self.start = 0

        pyxel.fullscreen(True)
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def update(self):
        self.current_key = ''
        for letter in LETTERS:
            if pyxel.btn(getattr(pyxel,'KEY_'+letter)):
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
                    self.pb_time = (pyxel.frame_count-self.start)//FPS
                    self.start = pyxel.frame_count

                self.text.__init__(self.txtList,self.text.index)
        
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,self.text.typed,9)
        pyxel.text(10+4*self.text.pos,10,self.text.remaining,7)
        pyxel.text(10+4*self.text.pos,13,'_',11)
        pyxel.text(10+self.text.camx,30,'Time: '+str((pyxel.frame_count-self.start)//FPS),8)
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