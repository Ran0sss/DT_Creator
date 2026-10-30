DT CREATOR — PROTOTYPE 0.3.3
=============================

OBJECTIF
Cette distribution isole les dependances Python de DT Creator dans un
environnement local .venv, sans utiliser l'environnement Anaconda existant.

PREMIER LANCEMENT (version Python)
1. Decompresser tout le dossier DT_Creator dans un emplacement accessible.
2. Installer Python 3.11 ou 3.12 (64 bits) depuis python.org si necessaire.
3. Double-cliquer sur Installer_Environnement.bat.
   - Cree .venv dans ce dossier.
   - Installe les dependances depuis requirements.txt (connexion Internet requise).
4. Double-cliquer sur Lancer_DT.bat.
5. L'interface s'ouvre dans le navigateur.

LANCEMENTS SUIVANTS
Double-cliquer uniquement sur Lancer_DT.bat.

CONSTRUIRE UNE VERSION EXE
Sur un poste Windows de construction avec Python :
1. Lancer Installer_Environnement.bat.
2. Lancer Construire_Paquet_Windows.bat.
3. Le resultat est dist\DT_Creator\DT_Creator.exe.
4. Pour diffusion, copier le dossier dist\DT_Creator COMPLET.
   Ne pas distribuer le seul fichier EXE.

LIMITES ET PREREQUIS
- La version archive avec .venv requiert Python sur le poste cible et Internet
  au premier setup pour telecharger les dependances.
- La version EXE PyInstaller ne requiert normalement pas Python/Anaconda chez
  l'utilisateur final. Elle doit etre construite et validee sur Windows.
- Le paquet EXE est ici construit en mode onedir (dossier de fichiers), plus
  fiable pour Streamlit que le mode onefile. Une archive ZIP de dist\DT_Creator
  peut etre partagee.
- Les dependances sont des plages de versions, pas encore un verrouillage
  reproductible. Une phase de validation devra figer les versions testees.
- Au premier lancement, verifier les alertes SmartScreen/antivirus selon la
  politique informatique de l'organisation.

VERSION 0.3.3.1
- Correctif du detecteur Python : recherche aussi C:\\Anaconda3 et installations Python usuelles.
- Si Anaconda est installe dans son emplacement de developpement habituel, le setup peut creer .venv a partir de cet interpreteur.

VERSION 0.3.3
- Ajout d'un setup d'environnement Python isole (.venv).
- Lancement prioritaire depuis cet environnement, sans chemin Anaconda.
- Script de construction PyInstaller mis a jour.
- Fonctionnalites de l'application conservees depuis le prototype 0.3.2.
