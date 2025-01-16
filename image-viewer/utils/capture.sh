#!/bin/bash

# Check if required commands exist
check_commands() {
    for cmd in ffmpeg yt-dlp; do
        if ! command -v $cmd &> /dev/null; then
            echo "Error: $cmd is not installed"
            echo "Please install $cmd and try again"
            exit 1
        fi
    done
}

# Print usage information
print_usage() {
    echo "Usage: $0 <YouTube_URL> <output_name>"
    echo ""
    echo "Arguments:"
    echo "  YouTube_URL: URL of the YouTube video"
    echo "  output_name: Base name for output files (will be appended with _1.jpg, _2.jpg, etc.)"
    echo ""
    echo "Example:"
    echo "  $0 \"https://youtube.com/watch?v=...\" \"frame\""
    echo "  This will create frame_1.jpg, frame_2.jpg, etc."
}

# Main script
main() {
    # Check for required commands
    check_commands

    # Check if correct number of arguments provided
    if [ $# -ne 2 ]; then
        echo "Error: Incorrect number of arguments"
        print_usage
        exit 1
    fi

    URL="$1"
    NAME="$2"

    echo "Extracting frames from: $URL"
    echo "Output files will be named: ${NAME}_N.jpg"

    # Execute the frame extraction
    ffmpeg -i $(yt-dlp -f best -g "$URL") -vf fps=1 "${NAME}_%d.jpg"

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Frame extraction completed successfully"
    else
        echo "Error: Frame extraction failed"
        exit 1
    fi
}

# Run the script
main "$@"
