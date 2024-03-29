from datetime import datetime
from textgenrnn import textgenrnn

MODEL_NAME = '800k_c_128_4_025'

USE_PROMPT = True  # True s interactive, False makes txt files with config below

EPOCHS = [0]

TEMPERATURES = [
        [1.0, 0.3, 0.2, 0.1],
        [1.0, 0.9, 0.2, 0.2, 0.2, 0.2],
        [1.0, 0.5, 0.2, 0.2],
        [1.0, 0.7, 0.4, 0.4],
        [0.9, 0.9, 0.5, 0.2, 0.2, 0.2],
        [0.8, 0.2, 0.8, 0.2]
    ]

NUM_SAMPLES = 150
MAX_GEN_LENGTH = 300
GEN_PREFIX = None


def gen_prompt(epoch=0):

    if epoch == 0:
        weights = 'models/{}/{}_weights.hdf5'.format(MODEL_NAME, MODEL_NAME)
    else:
        weights = 'epochs/{}_weights_epoch_{}.hdf5'.format(MODEL_NAME, epoch)

    vocab = 'models/{}/{}_vocab.json'.format(MODEL_NAME, MODEL_NAME)
    config = 'models/{}/{}_config.json'.format(MODEL_NAME, MODEL_NAME)

    textgen = textgenrnn(weights_path=weights
                        ,vocab_path=vocab
                        ,config_path=config)

    print(textgen.model.summary())

    while True:
        prefix = input("Prefix : ")
        try:
            temp = float(input("Temp : "))
        except:
            temp = 0.3
        try:
            samples = int(input("Samples : "))
        except:
            samples = 2
        try:
            length = int(input("Max Length : "))
        except:
            length = 100
        tts = True if input("tts [y/n] : ")=="y" else False
        generated_texts = textgen.generate(n=samples
                                        ,prefix=prefix
                                        ,temperature=temp
                                        ,max_gen_length=length
                                        ,return_as_list=True)
        if tts:
            import pyttsx3 # pip install pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 140)
            engine.setProperty('volume',1.0)
            engine.setProperty('voice', engine.getProperty('voices')[0].id)

        for text in generated_texts:
            print(text)
            if tts:
                engine.say(text)
                engine.runAndWait()
                engine.stop()


def gen_txt(epochs=[0], temperatures=[1.0], samples=10, max_len=300, prefix=None):

    vocab = 'models/{}/{}_vocab.json'.format(MODEL_NAME,MODEL_NAME)
    config = 'models/{}/{}_config.json'.format(MODEL_NAME,MODEL_NAME)

    for epoch in epochs:

        if epoch == 0:
            weights = 'models/{}/{}_weights.hdf5'.format(MODEL_NAME,MODEL_NAME)
        else:
            weights = 'models/{}/epochs/{}_weights_epoch_{}.hdf5'.format(MODEL_NAME,MODEL_NAME,epoch)

        textgen = textgenrnn(weights_path=weights
                            ,vocab_path=vocab
                            ,config_path=config)

        for temp in temperatures:
            timestring = datetime.now().strftime('%Y%m%d_%H%M%S')
            gen_file = '{}_gentext_{}_epoch_{}_temp_{}.txt'.format(MODEL_NAME,timestring, epoch, str(temp))
            textgen.generate_to_file(gen_file
                                    ,n=samples
                                    ,prefix=prefix
                                    ,temperature=temp
                                    ,max_gen_length=max_len)

if __name__ == "__main__":
    if USE_PROMPT:
        gen_prompt(EPOCHS[0])
    else:
        gen_txt(EPOCHS, TEMPERATURES
            ,samples=NUM_SAMPLES
            ,max_len=MAX_GEN_LENGTH
            ,prefix=GEN_PREFIX)