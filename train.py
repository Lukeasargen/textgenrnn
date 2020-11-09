import os
import json
from datetime import datetime
from textgenrnn import textgenrnn


def main():
    model_cfg = {
        'rnn_size': 64, # number of LSTM cells of each layer (128/256 recommended)
        'rnn_layers': 2, # number of LSTM layers (>=2 recommended)
        'rnn_bidirectional': True, # consider text both forwards and backward, can give a training boost
        # (20-40 for characters, 5-10 for words recommended)
        'max_length': 32, # number of tokens to consider before predicting the next
        'max_words': 1024, # maximum number of words to model; the rest will be ignored (word-level model only)
        'dim_embeddings': 80,
        'word_level': False, # set to True if want to train a word-level model (requires more data and smaller max_length)
    }

    train_cfg = {
        'line_delimited': False, # set to True if each text has its own line in the source file
        'num_epochs': 300, # set higher to train the model for longer
        'gen_epochs': 10, # generates sample text from model after given number of epochs
        'save_epochs': 10,
        'batch_size': 1024,
        'train_size': 1.0, # proportion of input data to train on: setting < 1.0 limits model from learning perfectly
        'dropout': 0.7,
        'max_gen_length': 60,
        'validation': False, # If train__size < 1.0, test on holdout dataset; will make overall training slower
        'is_csv': False # set to True if file is a CSV exported from Excel/BigQuery/pandas
    }

    model_name = 'frank_channel_orange_c_48_2_070'

    new_model = True  # False for retraining
    text_file = 'datasets/frank_channel_orange.txt'  # new model trains on this file
    # text_file = 'dev/150k.txt'  # new model trains on this file

    """retraining settings below"""
    # If new_model=false, these are the files used for training
    epoch = 0 # what epoch to resume training. 0 loads the last complete epoch
    files = ['dev/40kold1.txt',
             'dev/40kold2.txt']

    # Generatates lot's of samples during retraining
    temperatures = [
                    [1.0, 0.5, 0.2, 0.2],
                    [0.9, 0.9, 0.5, 0.2, 0.2, 0.2],
                    [0.8, 0.2, 0.8, 0.2],
                    [1.0, 0.7, 0.2, 0.1, 0.6, 0.2]
                    ]
    n = 200   # number of texts to generate: set much higher if model was trained as line-delimited
    max_gen_length = 500   # maximum size of each text: set much higher if model was trained as a single-file
    prefix = None

    if new_model:

        print("---- Creating a new model... ----")

        textgen = textgenrnn(name=model_name)

        print("---- New model started ----")

        print("Source :", text_file)
        print("Model :", model_cfg)
        print("Train :", train_cfg)

        train_function = textgen.train_from_file if train_cfg['line_delimited'] else textgen.train_from_largetext_file

        # https://colab.research.google.com/drive/1mMKGnVxirJnqDViH7BDJxFqWrsXlPSoK
        train_function(
            file_path=text_file,
            new_model=True,
            num_epochs=train_cfg['num_epochs'],
            gen_epochs=train_cfg['gen_epochs'],
            save_epochs=train_cfg['save_epochs'],
            batch_size=train_cfg['batch_size'],
            train_size=train_cfg['train_size'],
            dropout=train_cfg['dropout'],
            max_gen_length=train_cfg['max_gen_length'],
            validation=train_cfg['validation'],
            is_csv=train_cfg['is_csv'],
            rnn_size=model_cfg['rnn_size'],
            rnn_layers=model_cfg['rnn_layers'],
            rnn_bidirectional=model_cfg['rnn_bidirectional'],
            max_length=model_cfg['max_length'],
            max_words=model_cfg['max_words'],
            dim_embeddings=model_cfg['dim_embeddings'],
            word_level=model_cfg['word_level']
        )

        print(textgen.model.summary())

    else:
        # Only need these once
        vocab = 'models/{}/{}_vocab.json'.format(model_name, model_name)

        config = 'models/{}/{}_config.json'.format(model_name, model_name)

        with open(config) as config_file:
            data = json.load(config_file)

        for i in range(len(files)):

            if i == 0:  # handle the first differently
                if epoch == 0:
                    weights = 'models/{}/{}_weights.hdf5'.format(model_name,model_name)
                else:
                    weights = 'epochs/{}/{}_weights_epoch_{}.hdf5'.format(model_name,model_name,epoch)
            else:  # after the first one, then load from current directory bc that's were textgenrnn saves
                weights = '{}_weights.hdf5'.format(model_name)

            print("Loading old model...")

            textgen = textgenrnn(name=model_name,
                                weights_path=weights,
                                vocab_path=vocab,
                                config_path=config)

            print(textgen.model.summary())

            print("Source :", files[i])
            print("Train :", train_cfg)

            train_function = textgen.train_from_largetext_file if data["single_text"] else textgen.train_from_file

            train_function(
                file_path=files[i],
                new_model=False,
                num_epochs=train_cfg['num_epochs'],
                gen_epochs=train_cfg['gen_epochs'],
                save_epochs=train_cfg['save_epochs'],
                batch_size=train_cfg['batch_size'],
                train_size=train_cfg['train_size'],
                dropout=train_cfg['dropout'],
                max_gen_length=train_cfg['max_gen_length'],
                validation=train_cfg['validation'],
                is_csv=train_cfg['is_csv']
            )

            print("\nGenerating sample files\n")

            for temp in temperatures:
                timestring = datetime.now().strftime('%Y%m%d_%H%M%S')
                gen_file = '{}_gentext_{}_epoch_{}_temp_{}.txt'.format(model_name,timestring, epoch, str(temp))
                textgen.generate_to_file(gen_file,
                                        n=n,
                                        prefix=prefix,
                                        temperature=temp,
                                        max_gen_length=max_gen_length)


if __name__ == "__main__":
    main()