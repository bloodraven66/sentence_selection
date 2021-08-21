#!/usr/bin/env bash
python3 main.py --triphone-file=../computedSplits/triphoneSet.pkl \
                --audio-path ../../../other_tts_data/LJSpeech-1.1/wavs/ \
                --method=random \
                --save-path=../data_folder_demo/ \
                --mode=skewed \
                --dur-in-hours=0.1 \
                --cache-audio-dur=../data_folder_demo/ \
                --dataset-identifier=ljspeech
