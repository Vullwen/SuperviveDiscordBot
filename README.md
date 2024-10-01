# SuperVive Discord Bot

Le bot SuperVive est un bot Discord conçu pour fournir des statistiques de jeu et des informations aux utilisateurs en utilisant l'API SuperVive. Ce bot permet aux utilisateurs d'accéder facilement à des statistiques de jeu telles que les statistiques de héros (tier lists) et les statistiques des joueurs, directement depuis Discord.

## Fonctionnalités

- **Tierlist Command**: Obtenez la liste de niveaux pour un mode de jeu spécifique avec des options de tri.
- **Stats Command**: Recherchez et obtenez les statistiques détaillées d'un joueur:
    - Statistiques générales du joueur
    - Statistiques de jeu par champion, et par mode


## Fichiers

### `main.py`
Ce fichier contient le code principal du bot Discord, y compris la définition des commandes, l'initialisation du bot et la gestion des interactions utilisateur. Il utilise `py-cord` pour l'interaction avec l'API Discord.

### `api.py`
Ce fichier définit la classe `SuperViveAPI`, qui encapsule les appels à l'API SuperVive de https://supervive.io . Il comprend des méthodes pour obtenir les statistiques, rechercher des joueurs, et récupérer des images de héros.

### `config.py`
Ce fichier contient les configurations nécessaires pour le fonctionnement du bot. Il inclut le jeton d'authentification, la liste des propriétaires, les statuts du bot, ainsi que les URL de l'API et des assets.

```python
import os

TOKEN = "xxx"

status = [
    "Status1",
    "Status2",
    "Status3"
]

owners = [1234567890]

API = "https://link.api"
ASSETS = "https://assets.link"
```

#### Explications du `config.py`

- `TOKEN`: Ce jeton est utilisé pour authentifier le bot avec l'API Discord. **Note**: Ce jeton est sensible et ne doit pas être partagé ou exposé publiquement.
- `status`: Liste des statuts que le bot affichera de manière cyclique.
- `owners`: Liste des identifiants des propriétaires du bot, permettant des permissions spéciales.
- `API`: URL de base pour accéder à l'API SuperVive.
- `ASSETS`: URL de base pour accéder aux ressources graphiques (comme les images des héros).

## Installation et Exécution

1. Clonez ce dépôt.
2. Installez les dépendances avec `pip install -r requirements.txt`.
3. Ajoutez votre jeton Discord et autres configurations nécessaires dans le fichier `config.py`.
4. Exécutez le bot avec `python main.py`.

# SuperVive Discord Bot

Le bot SuperVive est un bot Discord conçu pour fournir des statistiques de jeu et des informations aux utilisateurs en utilisant l'API SuperVive. Ce bot permet aux utilisateurs d'accéder facilement à des statistiques de jeu telles que les statistiques de héros (tier lists) et les statistiques des joueurs, directement depuis Discord.

## Fonctionnalités

- **Tierlist Command**: Obtenez la liste de niveaux pour un mode de jeu spécifique avec des options de tri.
- **Stats Command**: Recherchez et obtenez les statistiques détaillées d'un joueur:
    - Statistiques générales du joueur
    - Statistiques de jeu par champion, et par mode


## Fichiers

### `main.py`
Ce fichier contient le code principal du bot Discord, y compris la définition des commandes, l'initialisation du bot et la gestion des interactions utilisateur. Il utilise `py-cord` pour l'interaction avec l'API Discord.

### `api.py`
Ce fichier définit la classe `SuperViveAPI`, qui encapsule les appels à l'API SuperVive de https://supervive.io . Il comprend des méthodes pour obtenir les statistiques, rechercher des joueurs, et récupérer des images de héros.

### `config.py`
Ce fichier contient les configurations nécessaires pour le fonctionnement du bot. Il inclut le jeton d'authentification, la liste des propriétaires, les statuts du bot, ainsi que les URL de l'API et des assets.

```python
import os

TOKEN = "xxx"

status = [
    "Status1",
    "Status2",
    "Status3"
]

owners = [1234567890]

API = "https://link.api"
ASSETS = "https://assets.link"
```

#### Explications du `config.py`

- `TOKEN`: Ce jeton est utilisé pour authentifier le bot avec l'API Discord. **Note**: Ce jeton est sensible et ne doit pas être partagé ou exposé publiquement.
- `status`: Liste des statuts que le bot affichera de manière cyclique.
- `owners`: Liste des identifiants des propriétaires du bot, permettant des permissions spéciales.
- `API`: URL de base pour accéder à l'API SuperVive.
- `ASSETS`: URL de base pour accéder aux ressources graphiques (comme les images des héros).

## Installation et Exécution

1. Clonez ce dépôt.
2. Installez les dépendances avec `pip install -r requirements.txt`.
3. Ajoutez votre jeton Discord et autres configurations nécessaires dans le fichier `config.py`.
4. Exécutez le bot avec `python main.py`.
