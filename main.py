import argparse
from handle_files import load_file
import get_stats
import method_parser

parser = argparse.ArgumentParser(description='Arguments for sentence selection')
parser.add_argument('--triphone-file', required=True, help='triphones for all sentences')
parser.add_argument('--mode', help='selection mode')
parser.add_argument('--dur-in-hours', required=True, type=float, help='duration of audio for selected sentences')
parser.add_argument('--dataset-identifier', required=True,  help='id to differntiate different datasets')
parser.add_argument('--audio-dur-file', default=None, help='triphones for all sentences')
parser.add_argument('--cache-audio-dur', default=None, help='Store durations for audio while running for the first time')
parser.add_argument('--override-caching', default=False, help='rewrite audio duration')
parser.add_argument('--audio-path', default=None, help='path to audio files')
parser.add_argument('--save-path', default=None, help='path to audio files')
parser.add_argument('--audio-extn', default='.wav', help='audio file extension')
parser.add_argument('--all-stats', default=True, type=bool, help='show high level info on triphone dictionary')
parser.add_argument('--method', required=True,  help='sentence selection method')
parser.add_argument('--config_folder', default='config', help='configuration for selection methods')

def main():
    dct, audio_files, audio_dur_dct = load_file(args)
    get_stats.execute(dct, status=args.all_stats)
    method_parser.run(dct, args, audio_files, audio_dur_dct)

if __name__ == '__main__':
    args = parser.parse_args()
    main()
