# Turing-Feathered-Fiasco-UI

The UI built in Python using PyGame which is to be used for the Apoorv Event hosted by Enigma Club of IIITK. Refer to the README file for further instructions and Rules. (Download the Zip File and start working on the model)

## Background:

Pebbles got carried away while playing and got stuck in a cavern full of icy pillars. Turing must go and save them, but the pillars are too high. Help Turing fly over the pillars and rescue Pebbles by building a model leveraging the power of AI/ML.

## SetUp:

Download the ZIP File and run the following command: `pip install -r /path/to/requirements.txt`

## Rules of the event:

- The participants must submit their models by 21st March, 11:59 pm
- The model size must not exceed 100 MB. (It includes the bird with the best gene and its respective config files)
- UI Source code link: [https://github.com/Enigma-IIITK/Turing-Feathered-Fiasco-UI.git]
- The fitness of the model will be evaluated through a mechanism that will not be revealed. The model with the highest fitness score will be crowned the winner.

## Rules of the game:

- The game is a modified version of the classic Flappy Bird game.
- There are:
  - 2 Holes with one of them having a coin. (The position of the coin is changed randomly)
  - 1 Bird (The submission should have only 1 bird with the best fitness).
- The frequency of the Pipes occurring will be increased by 8.33% after it crosses a score of 12 and by 16.67% after it crosses a score of 24.
- Gravity will be inverted throughout the game.
- There will be 2 holes in the pillars, each worth different points. The bird must learn to fly through the hole with the coin.

## Recommended frameworks

- Sci-Kit
- NEAT
- Pytorch Lightning
- TensorFlow Lite
- Keras RL

## Format of Submission

- 1 (.pkl) Pickle File which has the gene of the Best Bird.
  Use this function to export the best performing bird into a pickle file. (Also availabe in the UI .py File)
  `def Export(gen):
    global SCORE
    if SCORE > 40 :
        with open("submission.pkl", "wb") as f:
            print("!!!!!!!!!!!Saved!!!!!!!!!!")
            pickle.dump(gen, f)
            f.close()
            exit()`
- 1 (.py) Python File to load the data from the Pickle File and run the Bird (The UI along with the bot).
- 1 (.txt) Config File to set up the Neural Network.
