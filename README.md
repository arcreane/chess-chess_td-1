<<<<<<< HEAD
# Projet I1 — Jeu d'échecs Python

Projet d'échecs en Python orienté objet, conforme au cahier des charges :
- classes `Position`, `Piece`, `King`, `Queen`, `Bishop`, `Knight`, `Rook`, `Pawn`, `Board`, `Player`, `AIPlayer`, `Chess`
- utilisation d'une liste (`players`) et d'un dictionnaire (`Board.grid`)
- sauvegarde/restauration d'une partie au format JSON
- tests unitaires avec `unittest`
- interface texte + interface graphique Tkinter optionnelle

## Installation

```bash
python -m pip install -r requirements.txt
```

## Lancer en mode texte

```bash
python main.py
```

## Lancer en mode graphique

```bash
python gui.py
```

## Lancer les tests

```bash
python -m unittest discover tests
```

## Format des coups

Exemples :
- `Pe2 e4`
- `Nb1 c3`
- `Qd1 h5`

Commandes spéciales dans le jeu texte :
- `save partie.json`
- `load partie.json`
- `quit`

## Organisation Git recommandée

Branches possibles :
- `feature/position-board`
- `feature/piece-roi`
- `feature/piece-reine`
- `feature/piece-tour`
- `feature/piece-fou`
- `feature/piece-cavalier`
- `feature/piece-pion`
- `feature/save-load`
- `feature/interface-tkinter`

Messages de commit :
- `feat: add Position class`
- `feat: implement rook movement`
- `fix: prevent moving onto own piece`
- `test: add pawn movement tests`
=======
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ChwpCt9g)
>>>>>>> c56da763e11cb638d913691c3aa893c846366f7d
