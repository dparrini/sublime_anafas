import re
import sublime_plugin


class PlaceRulerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            ruler = RULER_DEFAULT
            line = self.view.line(region)
            
            iline, _ = self.view.rowcol(line.begin())
            print("Cursor at line", iline)
            card, at_line, ftype = parse_to_the_line(self.view, iline)

            if card is not None:
                if ftype == "P":
                    ruler_list = card_rulers_peco
                else:
                    ruler_list = card_rulers_anafas

                for icard, iruler in ruler_list.items():
                    if icard.upper() == card.upper():
                        ruler = iruler
                        break
            else:
                ruler = RULER_DEFAULT

            # insert ruler
            self.view.insert(edit, line.begin(), ruler + "\n")

            


# rulers by data card
RULER_DEFAULT = "("
RULER_TIPO = "( T"
RULER_TITU = "(---------------------Titulo do Caso------------------------------------------)"
RULER_CMNT = "(---------------------Comentários---------------------------------------------)"
RULER_BASE = "(---------------------Dados de BASE-------------------------------------------)"
RULER_DARE = "(NN  C                            NOME\n(--  =            ------------------------------------"
RULER_DMOV = "(BF  C   BT  NC  VBAS   Ipr      Imax     Emax     Pmax\n(                (kV) (A rms)  (A rms)  (MJ/fas) (MW/fas)\n(--- -  ====---- ==== -------- ======== -------- ========"
RULER_DMUT = "(BF1 CE BT1   N1 BF2    BT2   N2  RM    XM     %I1   %F1   %I2   %F2  IA SA\n(----=-=====  ==-----  =====  ==------====== ------======------======--- =="
RULER_DSHL = "(BF  CE BT    NCTNG  Qpos  L  Rn    Xn  E Nome  NunNop               IA  SA                                     Nome Extendido\n(====-=-----  ==-== ====== =------======-====== ===---               === ==                                     ===================="
RULER_DEOL = "(NB  CE       NG P_inic I_max V_min F_potNNNNNN NunNop               AAA\n(====-=      === ======------======------====== ===---               ==="
RULER_DREB = "("
RULER_DCIR_PECO   = "(BF  CE  BT   NCT  R1    X1    R0    X0    CN                  TB  TCIA DEF  KM CD RNDE  XNDE CP RNPA  XNPA SA     NunNop DJ_BF CicDJ_BT Cic                    DDMMAAAADDMMAAAA M.V.A              TD     NOME EXTENSO\n(----=-=====  --=------======------======------               -----==---=== ====--======------==------======---    ===--- ======---======---                    ========-------- =====              == --------------------"
RULER_DBAR_PECO   = "(NB  CEM      BN               VBAS DISJUN          DDMMAAAADDMMAAAA IA SA  F\n(----=-= ------------          ---- ------          --------======== ---=== -"
RULER_DCIR_ANAFAS = "(BF  CE  BT   NCT  R1    X1    R0    X0    CN   S1   S0   TAP  TB  TCIA DEFE KM CD RNDE  XNDE CP RNPA  XNPA SA     NunNop DJ_BF CicDJ_BT Cic                    DDMMAAAADDMMAAAA M.V.A              TD     NOME EXTENSO\n(----=-=====  --=------======------======------=====-----=====-----==---===-====--======------==------======---    ===--- ======---======---                    ========-------- =====              == --------------------"
RULER_DBAR_ANAFAS = "(NB  CEM      BN      VPRE ANG VBAS DISJUN          DDMMAAAADDMMAAAA IA SA\n(----=-= ------------ ----==== ---- ------          --------======== ---==="

# card names
CARD_TIPO = "TIPO"
CARD_TITU = "TITU"
CARD_CMNT = "CMNT"
CARD_BASE = "BASE"
CARD_DMUT = "DMUT"
CARD_DMOV = "DMOV"
CARD_DSHL = "DSHL"
CARD_DEOL = "DEOL"
CARD_DARE = "DARE"
CARD_DREB = "DREB"
CARD_DBAR = "DBAR"
CARD_DCIR = "DCIR"
CARD_FIM  = "FIM"

# alternative card names
alt_cards = [
    [CARD_TIPO, "(?i)^(" + CARD_TIPO + "|  0)\\s*$"],
    [CARD_TITU, "(?i)^(" + CARD_TITU + "|  1)\\s*[0-9]?[0-9]?\\s*$"],
    [CARD_CMNT, "(?i)^(" + CARD_CMNT + "|  2)\\s*[0-9]?[0-9]?\\s*$"],
    [CARD_BASE, "(?i)^(" + CARD_BASE + "|100)\\s*$"],
    [CARD_DMUT, "(?i)^(" + CARD_DMUT + "| 39)\\s*$"],
    [CARD_DMOV, "(?i)^(" + CARD_DMOV + "| 36)\\s*$"],
    [CARD_DSHL, "(?i)^(" + CARD_DSHL + "| 35)\\s*$"],
    [CARD_DEOL, "(?i)^(" + CARD_DEOL + ")\\s*$"],
    [CARD_DARE, "(?i)^(" + CARD_DARE + ")\\s*$"],
    [CARD_DREB, "(?i)^(" + CARD_DREB + ")\\s*$"],
    [CARD_DBAR, "(?i)^(" + CARD_DBAR + "| 38)\\s*$"],
    [CARD_DCIR, "(?i)^(" + CARD_DCIR + "| 37)\\s*$"],
    [CARD_FIM , "(?i)^(" + CARD_FIM  + "| 99)\\s*$"]
]

# data card ending
card_endings = ["99999", "F"]

# PECO format rulers dictionary
card_rulers_peco = {
    CARD_TIPO: RULER_TIPO,
    CARD_TITU: RULER_TITU,
    CARD_CMNT: RULER_CMNT,
    CARD_BASE: RULER_BASE,
    CARD_DARE: RULER_DARE,
    CARD_DMOV: RULER_DMOV,
    CARD_DMUT: RULER_DMUT,
    CARD_DSHL: RULER_DSHL,
    CARD_DEOL: RULER_DEOL,
    CARD_DREB: RULER_DREB,
    CARD_DCIR: RULER_DCIR_PECO,
    CARD_DBAR: RULER_DBAR_PECO,
    CARD_FIM:  RULER_DEFAULT
}

# ANAFAS format rulers dictionary
card_rulers_anafas = dict(card_rulers_peco)
card_rulers_anafas[CARD_DCIR] = RULER_DCIR_ANAFAS
card_rulers_anafas[CARD_DBAR] = RULER_DBAR_ANAFAS


def parse_to_the_line(view, line):
    ftype = "P"
    card = None
    at_line = line

    for iline in range(line, -1, -1):
        point = view.text_point(iline, 0)
        content = view.substr(view.line(point))
        print("Going up:", content)
        card = is_card(content, alt_cards)
        if card is not None:
            print("Card found!", card)
            at_line = iline
            break

    return card, at_line, ftype


def is_card(content, cards):
    card = None
    for icards in cards:
        actual_card = icards[0]
        card_regex = re.compile(icards[1])

        if card_regex.match(content) is not None:
            card = actual_card
            break
    return card

