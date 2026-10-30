import json, math, re, uuid
from datetime import date, datetime
import streamlit as st

VERSION="0.3.3"
COMMON=set("Al Ag Au B C Co Cr Cu Fe In Mg Mn Mo N Nb Ni O P Pt S Re Ru Si Sn Ta Ti V W Y Zr".split())
NAMES={
"H":"Hydrogène","He":"Hélium","Li":"Lithium","Be":"Béryllium","B":"Bore","C":"Carbone","N":"Azote","O":"Oxygène","F":"Fluor","Ne":"Néon",
"Na":"Sodium","Mg":"Magnésium","Al":"Aluminium","Si":"Silicium","P":"Phosphore","S":"Soufre","Cl":"Chlore","Ar":"Argon",
"K":"Potassium","Ca":"Calcium","Sc":"Scandium","Ti":"Titane","V":"Vanadium","Cr":"Chrome","Mn":"Manganèse","Fe":"Fer","Co":"Cobalt","Ni":"Nickel","Cu":"Cuivre","Zn":"Zinc",
"Ga":"Gallium","Ge":"Germanium","As":"Arsenic","Se":"Sélénium","Br":"Brome","Kr":"Krypton","Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium","Nb":"Niobium","Mo":"Molybdène","Tc":"Technétium","Ru":"Ruthénium","Rh":"Rhodium","Pd":"Palladium","Ag":"Argent","Cd":"Cadmium","In":"Indium","Sn":"Étain","Sb":"Antimoine","Te":"Tellure","I":"Iode","Xe":"Xénon",
"Cs":"Césium","Ba":"Baryum","La":"Lanthane","Ce":"Cérium","Pr":"Praséodyme","Nd":"Néodyme","Pm":"Prométhium","Sm":"Samarium","Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium","Ho":"Holmium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium","Lu":"Lutécium","Hf":"Hafnium","Ta":"Tantale","W":"Tungstène","Re":"Rhénium","Os":"Osmium","Ir":"Iridium","Pt":"Platine","Au":"Or","Hg":"Mercure","Tl":"Thallium","Pb":"Plomb","Bi":"Bismuth","Po":"Polonium","At":"Astate","Rn":"Radon",
"Fr":"Francium","Ra":"Radium","Ac":"Actinium","Th":"Thorium","Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium","Am":"Américium","Cm":"Curium","Bk":"Berkélium","Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendélévium","No":"Nobélium","Lr":"Lawrencium","Rf":"Rutherfordium","Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium","Mt":"Meitnérium","Ds":"Darmstadtium","Rg":"Roentgenium","Cn":"Copernicium","Nh":"Nihonium","Fl":"Flérovium","Mc":"Moscovium","Lv":"Livermorium","Ts":"Tennessine","Og":"Oganesson"}
# Periodic table cells by period/column (0..17).
ROWS=[
{0:"H",17:"He"},
{0:"Li",1:"Be",12:"B",13:"C",14:"N",15:"O",16:"F",17:"Ne"},
{0:"Na",1:"Mg",12:"Al",13:"Si",14:"P",15:"S",16:"Cl",17:"Ar"},
dict(enumerate("K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split())),
dict(enumerate("Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe".split())),
{0:"Cs",1:"Ba",2:"*",3:"Hf",4:"Ta",5:"W",6:"Re",7:"Os",8:"Ir",9:"Pt",10:"Au",11:"Hg",12:"Tl",13:"Pb",14:"Bi",15:"Po",16:"At",17:"Rn"},
{0:"Fr",1:"Ra",2:"**",3:"Rf",4:"Db",5:"Sg",6:"Bh",7:"Hs",8:"Mt",9:"Ds",10:"Rg",11:"Cn",12:"Nh",13:"Fl",14:"Mc",15:"Lv",16:"Ts",17:"Og"}]
LAN=["La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu".split(),"Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr".split()]
SPECIAL=set("O N H C S".split())
GROUP1=set("H Li Na K Rb Cs Fr".split())
UNAVAILABLE=set("He C N O F Ne Cl Ar Tc Te I Xe Po At Rn Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og Pm Ac Np Pu Cm Bk Cf Es Fm Md Lr".split())
st.set_page_config(page_title="DT Creator",page_icon="🧪",layout="wide")
st.title("🧪 DT Creator — demande d'analyse")
st.caption(f"Prototype autonome · version {VERSION} · export JSON")
st.header("1. Informations de la demande")
a,b=st.columns(2)
requester=a.text_input("Demandeur *")
aer=b.text_input("AER (facultatif)")
a,b=st.columns(2)
requested_on=a.date_input("Date de la demande",date.today())
observations=st.text_area("Observations générales (facultatif)",height=80)

st.header("2. Éléments à analyser")
if "picked" not in st.session_state: st.session_state.picked=set()
picked=set(st.session_state.picked)
def selected_banner(items):
    summary=", ".join(items) if items else "Aucun élément sélectionné"
    st.markdown(
        f"<div style='background:#e8f1fb;border:1px solid #b6d2ef;border-radius:8px;"
        f"padding:12px 16px;margin:0 0 12px 0;font-size:1.25rem;font-weight:600;"
        f"color:#1d3553'>Éléments sélectionnés ({len(items)}) : {summary}</div>",
        unsafe_allow_html=True)
# Styles communs : une seule règle pour toutes les tuiles, quel que soit leur état.
st.markdown("""
<style>
div[class*="st-key-tile_"] {
  height:56px; min-height:56px; box-sizing:border-box;
  padding:0 7px; border:1px solid #d6d8dc; border-radius:6px;
  display:flex; align-items:center; justify-content:center;
}
div[class*="st-key-tile_"] > div { width:100%; }
div[class*="st-key-tile_"] div[data-testid="stCheckbox"] {
  padding:0; margin:0; background:transparent; border:0;
}
div[class*="st-key-tile_"] div[data-testid="stCheckbox"] label {
  width:100%; display:flex; align-items:center; gap:7px;
}
div[class*="st-key-tile_"] div[data-testid="stCheckbox"] label p {
  margin:0; line-height:1; white-space:nowrap; font-size:0.95rem;
}
div[class*="st-key-tile_"] div[data-testid="stMarkdownContainer"] p {
  margin:0; line-height:1; text-align:center; font-size:0.95rem;
}
</style>
""", unsafe_allow_html=True)

def element_cell(sym):
    if sym in ("*","**") or sym not in NAMES:
        return
    disabled=(sym not in SPECIAL and (sym in GROUP1 or sym in UNAVAILABLE))
    color="#d9ead3" if sym in COMMON else "#fce5cd"
    if sym in SPECIAL: color="#cfe2f3"
    if disabled: color="#e2e3e5"
    # Une structure de conteneur identique pour toutes les tuiles.
    st.markdown(f"<style>.st-key-tile_{sym}{{background:{color};}}</style>", unsafe_allow_html=True)
    with st.container(border=False, key=f"tile_{sym}"):
        if disabled:
            st.markdown(f"<div style='height:54px;display:flex;align-items:center;justify-content:center;color:#858991'>{sym}</div>", unsafe_allow_html=True)
        else:
            state=st.checkbox(sym,value=(sym in picked),key=f"pick_{sym}")
            if state: picked.add(sym)
            else: picked.discard(sym)
for row in ROWS:
    cells=st.columns(18,gap="small")
    for j in range(18):
        with cells[j]:
            if j in row: element_cell(row[j])
            else: st.write(" ")
# Ligne blanche entre le tableau principal et le bloc f.
st.write("")
# Séries f : alignées de la colonne 3 à la colonne 17.
for series_idx, series in enumerate(LAN):
    cells=st.columns(18,gap="small")
    for c in range(18):
        with cells[c]:
            if 2 <= c <= 16:
                element_cell(series[c-2])
            else:
                st.write(" ")
st.markdown(
    "<div style='display:flex;gap:16px;flex-wrap:wrap;margin-top:8px;font-size:0.85rem'>"
    "<span>🟩 Élément usuel</span>"
    "<span>🟧 Faisabilité à confirmer</span>"
    "<span>🟦 IGA ONH/CS</span>"
    "<span>⬜ Non sélectionnable (colonne 1)</span>"
    "</div>", unsafe_allow_html=True
)
st.session_state.picked=picked
ordered=[sym for sym in NAMES if sym in picked]
selected_banner(ordered)
st.header("3. Échantillons")
n=int(st.number_input("Nombre d'échantillons",1,30,1,1))
samples=[]
for i in range(n):
    with st.expander(f"Échantillon {i+1}",expanded=(i==0)):
        a,b=st.columns([1,2])
        sid=a.text_input("Identifiant échantillon *",key=f"sid{i}",placeholder=f"Ex. ECH-{i+1:02d}")
        comment=b.text_input("Commentaire (facultatif)",key=f"comment{i}")
        samples.append({"sample_id":sid.strip(),"comment":comment.strip()})
st.header("4. Compositions attendues")
st.markdown("### Concentrations")
st.info("L’unité de déclaration est le % massique *(% m/m)*. Laisser le champ vide si concentration inconnue ; le zéro ne doit être renseigné que s’il est explicitement connu.")
comp=[]
for i,sample in enumerate(samples):
    with st.expander("Composition — "+(sample["sample_id"] or f"Échantillon {i+1}"),expanded=(i==0)):
        if i and st.button(f"Copier les concentrations de l'échantillon {i} vers celui-ci",key=f"copy{i}"):
            for el in ordered:
                st.session_state[f"conc{i}_{el}"]=st.session_state.get(f"conc{i-1}_{el}","")
            st.session_state[f"copied{i}"]=True
        if st.session_state.get(f"copied{i}"): st.success("Valeurs copiées. Tous les champs restent modifiables.")
        vals={}; cols=st.columns(4)
        for j,el in enumerate(ordered):
            with cols[j%4]:
                raw=st.text_input(el,key=f"conc{i}_{el}",placeholder="% massique").strip()
                if not raw: vals[el]=None
                else:
                    try:
                        v=float(raw.replace(",","."))
                        if not math.isfinite(v): raise ValueError()
                        vals[el]=v
                    except ValueError:
                        st.error(f"{el} : valeur invalide pour cet échantillon.")
                        vals[el]="__INVALID__"
        comp.append(vals)
st.header("5. Vérification et export")
errors=[]
if not requester.strip(): errors.append("Le demandeur est obligatoire.")
if not ordered: errors.append("Sélectionner au moins un élément.")
ids=[s["sample_id"] for s in samples]
if any(not x for x in ids): errors.append("Tous les identifiants d'échantillon sont obligatoires.")
canon=[re.sub(r"\s+"," ",x).casefold() for x in ids if x]
if len(canon)!=len(set(canon)): errors.append("Les identifiants doivent être uniques.")
if any("__INVALID__" in v.values() for v in comp): errors.append("Corriger les concentrations invalides.")
for e in errors: st.error(e)
if not errors: st.success(f"Demande prête : {n} échantillons · {len(ordered)} éléments.")
if st.button("Générer l'export JSON",type="primary",disabled=bool(errors)):
    data={"schema_version":"1.0","application":{"name":"DT Creator","version":VERSION},
      "request_id":str(uuid.uuid4()),"created_at":datetime.now().astimezone().isoformat(timespec="seconds"),
      "request":{"requester":requester.strip(),"aer":aer.strip() or None,"requested_on":requested_on.isoformat(),"observations":observations.strip() or None},
      "requested_elements":[{"symbol":s,"category":"ONH_CS" if s in SPECIAL else "OTHER"} for s in ordered],
      "concentration_unit":"% massique",
      "samples":[{"sample_id":s["sample_id"],"comment":s["comment"] or None,
        "composition":{"expected_concentrations":v,"unit":"% massique"}} for s,v in zip(samples,comp)],
      "notes":["Expected concentrations are requester-provided expectations, not measured results.",
       "null means not provided/unknown; zero is retained as an explicit numeric value.",
       "Concentrations use mass percent (% m/m). Copy action copies values into editable fields."]}
    serialized=json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)
    fname=f"Demande_DT_{datetime.now():%Y%m%d_%H%M%S}_{data['request_id'][:8]}.json"
    st.download_button("Télécharger le JSON",serialized.encode("utf-8"),fname,"application/json")
    st.subheader("Aperçu JSON"); st.code(serialized,language="json")
