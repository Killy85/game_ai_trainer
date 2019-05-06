# Install and and the game

## Requirements

- pygame
- keras
- tensorflow
- PLE (PyGame Learning Environment)

### tensorflow installation

> Windows installation is a bit complex, so i recommend to use linux to test the game

[Guide d'installation](https://www.tensorflow.org/install/pip)

### PLE installation

```shell
git clone https://github.com/ntasfi/PyGame-Learning-Environment
cd PyGame-Learning-Environment
pip install -e .
```

## Run the bot

### "homemade" game

```python
python3 snake_runner.py
```

### "PyGame Learning Environement" game

The game need a fps limitation, or it will have many bugs.

```python
python3 snake_ple_runner.py
```

# State description

The game is returning the actual state :

- Danger proximity (Front, Left, Right) : Warn if the player is near a danger. There is two dangers. First is collision with a border. Second is a collision with a body part.
- Food direction (Front, Left, Right) : Display in which direction player should look to get food.