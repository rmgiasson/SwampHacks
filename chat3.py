from spleeter.separator import Separator

def separate_audio():
    # Initialize the Spleeter separator with the 2-stems model
    separator = Separator('spleeter:2stems')

    # Provide the input file and output directory
    input_file = 'test_audio/star.mp3'
    output_dir = 'output'

    # Separate the track
    separator.separate_to_file(input_file, output_dir)

# Ensure the code is only executed when running as the main script
if __name__ == '__main__':
    separate_audio()