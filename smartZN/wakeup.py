import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=1024,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'cmusphinx-en-us-8khz-5.2'),
    lm=os.path.join(model_path, '6618.lm'),
    dic=os.path.join(model_path, '6618.dic')
)
def sphinx():
    for phrase in speech:
        print('返回:',phrase)
        # print(phrase.segments(detailed=True))
        if  str(phrase) == 'MOSS':
            print('唤醒')
            return  'wakeup'

# sphinx()