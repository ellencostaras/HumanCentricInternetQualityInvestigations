import ast
import re
import math
from tqdm import tqdm
import copy
import csv
import json
import csv
from datetime import datetime


#To run this code seemlessly, I recommend you change the following file paths to whatever
#is on your computer. Alternatively, if you've downloaded this from GitHub in the 
#"experiment1" folder, all the file paths should work automatically.

#file paths for testing_9_Aug
file_path_01 = "testing_stats/testing_9_Aug/call1_normal_latency.txt"
file_path_02 = "testing_stats/testing_9_Aug/call2_medium_latency.txt"
file_path_03 = "testing_stats/testing_9_Aug/call3_really_high_latency.txt"

#file path parent for testing_13_Aug
file_path_parent_01 = "testing_stats/testing_13_Aug/treatment" #*number* _ellen.txt or _aadya.txt
#e.g. "testing_stats/testing_13_Aug/treatment1_ellen.txt" or "testing_stats/testing_13_Aug/treatment4_aadya.txt"







#---------------- Finding all the stat names in the Web RTC dump ----------------

def get_key_names(file_path):
    
    '''
    This is the nested dictionary structure (starting with outermost):
    dump_file_name -> PeerConnections -> the 3rd dictionary (alphanumeric code) -> stats 
    
    This function exists just to print the names of all the statistics possible to select from. 
    '''
    
    with open(file_path, 'r') as file:
        dump = json.load(file)
    
    peer_connections = dump.get("PeerConnections", {})
    keys_list = list(peer_connections.keys())
    third_dictionary = peer_connections.get(keys_list[-1], {})
    stats = third_dictionary.get("stats", {})
    
    for key, value in stats.items():
        print(key)







#---------------- Parsing relevant stats ----------------

def get_call_identifiers(file_path):
    '''May need to implement this later for the real experiment'''
    
    #opening the dump .txt JSON file
    with open(file_path, 'r') as file:
        dump = json.load(file)
        
        #user_media = dump.get('getUserMedia', [])
    pass


def get_stats(file_path, verbose=False):
    '''
    This is the nested dictionary structure in the json .txt dump:
    dump_file_name -> PeerConnections -> the 3rd dictionary (alphanumeric code) -> stats 
    
    This function parses the relevant stats and saves them in custom data types (dictionaries).
    '''
    
    #opening the dump .txt JSON file
    with open(file_path, 'r') as file:
        dump = json.load(file)
    
    #navigate to where all the stats are stored in the dump
    peer_connections = dump.get('PeerConnections', {})
    keys_list = list(peer_connections.keys())
    third_dictionary = peer_connections.get(keys_list[-1], {})
    stats = third_dictionary.get('stats', {})
    
    #target substrings to pattern match for in stats
    target_substrings_IT01V = [
        '-[packetsReceived/s]',
        '-packetsLost', 
        '-frameWidth', 
        '-framesPerSecond', 
        '-totalFreezesDuration',
        '-[bytesReceived_in_bits/s]',
        '-totalProcessingDelay']
    target_substrings_IT01A = [
        '-[bytesReceived_in_bits/s]']
    target_substrings_OT01V = [
        '-[packetsSent/s]',
        '-[bytesSent_in_bits/s]',
        '-frameWidth',
        '-framesPerSecond',
        '-totalPacketSendDelay',
        '-[totalPacketSendDelay/packetsSent_in_ms]',
        '-qualityLimitationReason',
        '-qualityLimitationDurations',
        '-qualityLimitationResolutionChanges']
    target_substrings_RIV = [
        '-roundTripTime',
        '-fractionLost']
    target_substrings_RIA = [
        '-fractionLost']
    target_substrings_ROA = [
        '-roundTripTime']
    target_substrings_SV2 = [
        '-width',
        '-framesPerSecond']
    target_substrings_AP = [
        '-totalPlayoutDelay']
    
    #final dictionary data types to store all the values. 
    #each (None None None) triple will be filled with (values, start time, end time)
    target_values_dict_IT01V = {
        '-[packetsReceived/s]': (None, None, None),
        '-packetsLost': (None, None, None),
        '-frameWidth': (None, None, None),
        '-totalFreezesDuration': (None, None, None),
        '-framesPerSecond': (None, None, None),
        '-[bytesReceived_in_bits/s]': (None, None, None),
        '-totalProcessingDelay': (None, None, None),
        '-jitter': (None, None, None)}
    target_values_dict_IT01A = {
        '-[bytesReceived_in_bits/s]': (None, None, None)}
    target_values_dict_OT01V = {
        '-[packetsSent/s]': (None, None, None),
        '-[bytesSent_in_bits/s]': (None, None, None),
        '-frameWidth': (None, None, None),
        '-framesPerSecond': (None, None, None),
        '-totalPacketSendDelay': (None, None, None),
        '-[totalPacketSendDelay/packetsSent_in_ms]': (None, None, None),
        '-qualityLimitationReason': (None, None, None),
        '-qualityLimitationDurations': (None, None, None),
        '-qualityLimitationResolutionChanges': (None, None, None)}
    target_values_dict_RIV = {
        '-roundTripTime': (None, None, None),
        '-fractionLost': (None, None, None)}
    target_values_dict_RIA = {
        '-fractionLost': (None, None, None)}
    target_values_dict_ROA = {
        '-roundTripTime': (None, None, None)}
    target_values_dict_SV2 = {
        '-width': (None, None, None),
        '-framesPerSecond': (None, None, None)}
    target_values_dict_AP = {
        '-totalPlayoutDelay': (None, None, None)}
    
    #begin searching for the target statistics
    for key, value in stats.items():
        key_string = str(key)
        
        # inbound video ones
        if key_string[:5] == 'IT01V': 
            for target_substring in target_substrings_IT01V:
                if target_substring in key_string:
                    info = stats.get(key, {}) #jump into the innermost dictionary
                    if target_values_dict_IT01V[target_substring] == (None, None, None):
                        target_values_dict_IT01V[target_substring] = (info['values'], info['startTime'], info['endTime']) #just record whats in the values
            #special case for finding jitter because it is a substring of other keys too
            if key_string[-7:] == '-jitter':
                info = stats.get(key, {})
                if target_values_dict_IT01V['-jitter'] == (None, None, None):
                    target_values_dict_IT01V['-jitter'] = (info['values'], info['startTime'], info['endTime'])
        
        # inbound audio ones
        elif key_string[:5] == 'IT01A':
            for target_substring in target_substrings_IT01A:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_IT01A[target_substring] == (None, None, None):
                        target_values_dict_IT01A[target_substring] = (info['values'], info['startTime'], info['endTime'])
    
        # outbound video ones
        elif key_string[:5] == 'OT01V':
            for target_substring in target_substrings_OT01V:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_OT01V[target_substring] == (None, None, None):
                        target_values_dict_OT01V[target_substring] = (info['values'], info['startTime'], info['endTime'])
                    
        # remote inbound video ones
        elif key_string[:3] == 'RIV':
            for target_substring in target_substrings_RIV:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_RIV[target_substring] == (None, None, None):
                        target_values_dict_RIV[target_substring] = (info['values'], info['startTime'], info['endTime'])
        
        # remote inbound audio ones
        elif key_string[:3] == 'RIA':
            for target_substring in target_substrings_RIA:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_RIA[target_substring] == (None, None, None):
                        target_values_dict_RIA[target_substring] = (info['values'], info['startTime'], info['endTime'])
        
        # remote outbound audio ones
        elif key_string[:3] == 'ROA':
            for target_substring in target_substrings_ROA:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_ROA[target_substring] == (None, None, None):
                        target_values_dict_ROA[target_substring] = (info['values'], info['startTime'], info['endTime'])
                    
        # video source ones
        elif key_string[:3] == 'SV2':
            for target_substring in target_substrings_SV2:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_SV2[target_substring] == (None, None, None):
                        target_values_dict_SV2[target_substring] = (info['values'], info['startTime'], info['endTime'])
                    
        # audio playout ones
        elif key_string[:2] == 'AP':
            for target_substring in target_substrings_AP:
                if target_substring in key_string:
                    info = stats.get(key, {})
                    if target_values_dict_AP[target_substring] == (None, None, None):
                        target_values_dict_AP[target_substring] = (info['values'], info['startTime'], info['endTime'])
        
    if verbose:    
        print("\n\n---------------------------------INBOUND VIDEO STATS---------------------------------\n")
        for key, value in target_values_dict_IT01V.items():
            print(key, ": ", value[0])
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------INBOUND AUDIO STATS---------------------------------\n")
        for key, value in target_values_dict_IT01A.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------OUTBOUND VIDEO STATS---------------------------------\n")
        for key, value in target_values_dict_OT01V.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------REMOTE INBOUND VIDEO---------------------------------\n")
        for key, value in target_values_dict_RIV.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------REMOTE INBOUND AUDIO---------------------------------\n")
        for key, value in target_values_dict_RIA.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------REMOTE OUTBOUND AUDIO---------------------------------\n")
        for key, value in target_values_dict_ROA.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------VIDEO SOURCE STATS---------------------------------\n")
        for key, value in target_values_dict_SV2.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        print("\n\n---------------------------------AUDIO PLAYOUT STATS---------------------------------\n")
        for key, value in target_values_dict_AP.items():
            print(key, ": ", value)
            print("Start Time: ", value[1], " |  End Time: ", value[2])
            print("\n")
        
    return target_values_dict_IT01V, target_values_dict_IT01A, target_values_dict_OT01V, target_values_dict_RIV, target_values_dict_RIA, target_values_dict_ROA, target_values_dict_SV2, target_values_dict_AP









#---------------- Functions which convert/manipulate parsed data ----------------

def separate_by_comma(text_list):
    '''Function which takes a list in text form and converts it to a proper python list'''
    
    temp = ""
    list_list = []
    for char in text_list:
        if char == "[":
            temp = ""
        elif char == "]":
            try:
                list_list.append(float(temp))
            except ValueError:
                list_list.append(temp)
        elif char == ",":
            try:
                list_list.append(float(temp))
            except ValueError:
                list_list.append(temp)
            temp = ""
        else:
            temp = temp + char
    
    return list_list


def iso_to_unix_time(iso_string):
    '''funtion converting ISO time (like in Web RTC) to unix time'''

    dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    unix_time = int(dt.timestamp())
    return unix_time


def add_padding(data_dicts, global_start, global_end, verbose=False):
    '''Function to add -1s to all empty time entries'''
    
    new_data_dicts = []
    for dictionary in data_dicts:
        
        new_dictionary = {}
        for key, value in dictionary.items():
            start_time_unix = iso_to_unix_time(value[1])
            end_time_unix = iso_to_unix_time(value[2])
            start_padding = []
            end_padding = []
            
            if start_time_unix > global_start:
                start_padding = [-1] * (start_time_unix - global_start)
            if end_time_unix < global_end:
                end_padding = [-1] * (global_end - end_time_unix)
            
            if verbose:
                print("gs =", global_start, "stu =", start_time_unix, "lenfp =", len(start_padding))
                print("ge =", global_end, "etu =", end_time_unix, "lenep =", len(end_padding), "\n")

            new_values = start_padding + separate_by_comma(value[0]) + end_padding
            new_dictionary[key] = new_values
        
        new_data_dicts.append(new_dictionary)
    return new_data_dicts


def align_times(data_dicts_ellen, data_dicts_aadya, verbose=False):
    '''function which, for a single call, lines up all the times of the indivdual 
    stats by adding -1s for all seconds where there is no data.'''
    
    global_start = 999999999999999999999999
    global_end = 0
    
    for dictionary in data_dicts_ellen:
        for key, value in dictionary.items():
            start_time_unix = iso_to_unix_time(value[1])
            end_time_unix = iso_to_unix_time(value[2])
            if start_time_unix < global_start:
                global_start = start_time_unix
            if end_time_unix > global_end:
                global_end = end_time_unix
    
    for dictionary in data_dicts_aadya:
        for key, value in dictionary.items():
            start_time_unix = iso_to_unix_time(value[1])
            end_time_unix = iso_to_unix_time(value[2])
            if start_time_unix < global_start:
                global_start = start_time_unix
            if end_time_unix > global_end:
                global_end = end_time_unix
    
    new_data_dicts_ellen = add_padding(data_dicts_ellen, global_start, global_end, verbose)
    new_data_dicts_aadya = add_padding(data_dicts_aadya, global_start, global_end, verbose)
    return new_data_dicts_ellen, new_data_dicts_aadya  
            









#---------------- Functions which parse, then manipulate, then write data into a CSV ----------------

def parse_and_convert_to_csv_single_treatment(parent_file_path, treatment_number, verbose=False):
    '''function which creates a single CSV files for all the stats for a single call'''

    file_path_ellen = parent_file_path + str(treatment_number) + "_ellen.txt" #VERY IMPORTANT THAT FILE SUFFIXES
    file_path_aadya = parent_file_path + str(treatment_number) + "_aadya.txt" #CONFORM TO THIS CONVENTION!

    Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap = get_stats(file_path_ellen)
    Ait01v, Ait01a, Aot01v, Ariv, Aria, Aroa, Asv2, Aap = get_stats(file_path_aadya)
    
    all_ellens_data_unaligned = [Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap]
    all_aadyas_data_unaligned = [Ait01v, Ait01a, Aot01v, Ariv, Aria, Aroa, Asv2, Aap]
    all_ellens_data, all_aadyas_data = align_times(all_ellens_data_unaligned, all_aadyas_data_unaligned, verbose)
    
    #printing things if we want to:
    if verbose:
        for edict in range(len(all_ellens_data)):
            for key, val in all_ellens_data[edict].items():
                print("OG", key, ":", all_ellens_data_unaligned[edict][key][0])
                print("Start Time:", iso_to_unix_time(all_ellens_data_unaligned[edict][key][1]))
                print("END Time:", iso_to_unix_time(all_ellens_data_unaligned[edict][key][2]))
                print("NEW", key, ":", val, "\n")
        print("\n\n\n")
        for adict in range(len(all_aadyas_data)):
            for key, val in all_aadyas_data[adict].items():
                print("OG", key, ":", all_aadyas_data_unaligned[adict][key][0])
                print("Start Time:", iso_to_unix_time(all_aadyas_data_unaligned[adict][key][1]))
                print("END Time:", iso_to_unix_time(all_aadyas_data_unaligned[adict][key][2]))
            print("NEW", key, ":", val, "\n")

    dict_names = ["Inbound Video", "Inbound Audio", "Outbound Video", "Remote Inbound Video", "Remote Inbound Audio", "Remote Outbound Audio", "Source Video", "Audio Playback"]
    output_file = f"treatment{treatment_number}_13Aug.csv"
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for data_dict in range(len(all_ellens_data)):
            writer.writerow([])
            writer.writerow([dict_names[data_dict]])
            for key, value_list in all_ellens_data[data_dict].items():
                # Create a row where the first element is the key, followed by the values
                row1 = ["Ellen" + key] + value_list
                row2 = ["Aadya" + key] + all_aadyas_data[data_dict][key]
                # Write the rows to the CSV file
                writer.writerow(row1)
                writer.writerow(row2)

    print(f"Data has been written to {output_file}")
    
    
def parse_and_convert_to_csv_single_treatment_ellen_only(parent_file_path, treatment_number, verbose=False):
    '''function which creates a single CSV with all of Ellen's computer's stats for 
    a single call.'''
    
    file_path_ellen = parent_file_path + str(treatment_number) + "_ellen.txt"
    
    all_ellens_data_unaligned = [Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap]
    all_ellens_data, extra = align_times(all_ellens_data_unaligned, [], verbose)
    
    dict_names = ["Inbound Video", "Inbound Audio", "Outbound Video", "Remote Inbound Video", "Remote Inbound Audio", "Remote Outbound Audio", "Source Video", "Audio Playback"]
    output_file = f"treatment{treatment_number}_13Aug_ellen_only.csv"
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for data_dict in range(len(all_ellens_data)):
            writer.writerow([])
            writer.writerow([dict_names[data_dict]])
            for key, value_list in all_ellens_data[data_dict].items():
                # Create a row where the first element is the key, followed by the values
                row1 = ["Ellen" + key] + value_list
                # Write the rows to the CSV file
                writer.writerow(row1)
    print(f"Data has been written to {output_file}")

    
def parse_and_convert_to_csv_single_treatment_aadya_only(parent_file_path, treatment_number, verbose=False):
    '''function which creates a single CSV with all of Aadya's computer's stats for 
    a single call.'''
    
    file_path_aadya = parent_file_path + str(treatment_number) + "_aadya.txt"
    
    all_aadyas_data_unaligned = [Ait01v, Ait01a, Aot01v, Ariv, Aria, Aroa, Asv2, Aap]
    extra, all_aadyas_data = align_times([], all_aadyas_data_unaligned, verbose)
    
    dict_names = ["Inbound Video", "Inbound Audio", "Outbound Video", "Remote Inbound Video", "Remote Inbound Audio", "Remote Outbound Audio", "Source Video", "Audio Playback"]
    output_file = f"treatment{treatment_number}_13Aug_aadya_only.csv"
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for data_dict in range(len(all_aadyas_data)):
            writer.writerow([])
            writer.writerow([dict_names[data_dict]])
            for key, value_list in all_aadyas_data[data_dict].items():
                # Create a row where the first element is the key, followed by the values
                row2 = ["Aadya" + key] + all_aadyas_data[data_dict][key]
                # Write the rows to the CSV file
                writer.writerow(row2)
    print(f"Data has been written to {output_file}")


#FUNCTION I HAVENT FINISHED YET BUT WOULD CREATE A SINGLE CSV FILE WITH EVERY STAT FROM EVERY CALL 
'''def parse_and_convert_into_csv_all_treatments(parent_file_path, total_number_of_treatments):
    
    output_file = "all_stats_all_treatments_13Aug"
    dict_names = ["Inbound Video", "Inbound Audio", "Outbound Video", "Remote Inbound Video", "Remote Inbound Audio", "Remote Outbound Audio", "Source Video", "Audio Playback"]
    
    header = ["Statistic"]
    for i in range(total_number_of_treatments):
        header.append(f"treatment{i}")
        
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        
        file_path_ellen = parent_file_path + str(treatment_number) + "_ellen.txt"
        all_ellens_data = [Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap]
        
    file_path_aadya = parent_file_path + str(treatment_number) + "_aadya.txt"

    Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap = get_stats(file_path_ellen)
    Ait01v, Ait01a, Aot01v, Ariv, Aria, Aroa, Asv2, Aap = get_stats(file_path_aadya)
    
    all_ellens_data = [Eit01v, Eit01a, Eot01v, Eriv, Eria, Eroa, Esv2, Eap]
    all_aadyas_data = [Ait01v, Ait01a, Aot01v, Ariv, Aria, Aroa, Asv2, Aap]
    
    for dictionary in range(len(all_ellens_data)):
        for key, value in all_ellens_data[dictionary].items():
            all_ellens_data[dictionary][key] = separate_by_comma(value)
    for dictionary in range(len(all_aadyas_data)):
        for key, value in all_aadyas_data[dictionary].items():
            all_aadyas_data[dictionary][key] = separate_by_comma(value)
    
    dict_names = ["Inbound Video", "Inbound Audio", "Outbound Video", "Remote Inbound Video", "Remote Inbound Audio", "Remote Outbound Audio", "Source Video", "Audio Playback"]
'''