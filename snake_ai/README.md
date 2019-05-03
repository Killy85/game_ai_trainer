# Installation et lancement du jeu

## Requirements

- pygame
- keras
- tensorflow
- PLE (PyGame Learning Environment)

### Installation de tensorflow

> L'installation est trop complexe sur Windows

[Guide d'installation](https://www.tensorflow.org/install/pip)

### Installation de PLE

```shell
git clone https://github.com/ntasfi/PyGame-Learning-Environment
cd PyGame-Learning-Environment
pip install -e .
```

## Lancement du bot

### Avec le jeu "maison"

```python
python3 snake_runner.py
```

### Avec le jeu de PyGame Learning Environement

Le jeu a besoin d'une limite de FPS sinon il se retrouve à buguer.

```python
python3 snake_ple_runner.py
```

# Description des états

Le jeu retourne les informations suivantes :

- Position X du joueur
- Position Y du joueur
- Zone de danger (Front, Left, Right) : Indique si la zone autour du joueur est dangeureuse. Soit à cause d'une bordure, soit à cause d'une partie du corps du joueur
- Zone de nourriture (Front, Left, Right) : Indique si la zone autour du joueur a de la nourriture.