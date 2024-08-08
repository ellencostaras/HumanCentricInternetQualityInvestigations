#!/bin/bash

# Define the function that performs the main task
perform_task() {
    echo -e "\nBeginning experiment..."
    read -p "Please enter the treatment number you wish to engage: " numberEntered

    treatment=$((numberEntered + 1))

    # Fetch the row from the CSV
    row=$(awk -F, -v row=$treatment 'NR==row {print $0}' test_combos_shuffled.csv)

    if [ -z "$row" ]; then
        echo "Invalid treatment number. Please try again."
        return
    fi

    # Extract values from the row
    IFS=',' read -r treatmentNo upVal downVal rttVal packVal <<< "$row"

    echo -e "\nTEMPORARY FEATURE OF PRINTING THROTTLE VALUES WHILE STILL TESTING:"
    echo "Treatment number: $treatmentNo"
    echo "upload (kbps): $upVal"
    echo "download (kbps): $downVal"
    echo "rtt (ms): $rttVal"
    echo "packet loss (%): $packVal"
    echo -e "\n"

    read -p "Type any character and press Enter to engage throttle: " dummy3
    # Engage throttle
    throttle --up $upVal --down $downVal --rtt $rttVal --packetLoss $packVal
    clear
    echo "throttle enagaged."

    echo -e "\nAllow 10-20 seconds before commencing Zoom call.\n"
    read -p "Type any character and press Enter when ready to stop throttling: " dummy2
    clear

    # Stop throttle
    throttle --stop
}

# Define the function that handles user interaction and repetition
main_loop() {
    while true; do
        perform_task

        while true; do
            read -p "Do you want to perform the function again or exit entirely? (Again/Exit): " choice
            case "$choice" in
                Again|again)
                    break
                    ;;
                Exit|exit)
                    echo -e "Exiting the experiment.\n"
                    exit 0
                    ;;
                *)
                    echo "Invalid input. Please type 'Again' or 'Exit'."
                    ;;
            esac
        done
    done
}

# Start the script by calling the main loop function
clear
echo "Welcome to the Down-throttling Experiment Environment!"
echo -e "\nPlease ensure you have npm and throttle downloaded already."

read -p "Please type any character and press Enter to begin: " dummy1

main_loop

