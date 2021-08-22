#!/usr/bin/env bash
python3 main.py --triphone-file=../computedSplits/triphoneSet.pkl \
                --audio-path ../../../other_tts_data/LJSpeech-1.1/wavs/ \
                --method=low_triphone_count_priority \
                --save-path=../data_folder_demo/ \
                --mode=uniform \
                --dur-in-hours=1.5 \
                --cache-audio-dur=../data_folder_demo/ \
                --dataset-identifier=ljspeech
