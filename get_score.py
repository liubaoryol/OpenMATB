"""
Script to calculate the score of the performance on secondary tasks.

File name is the only obligatory argument.
No need of specifying the secondary task (communication/sysmon)
"""
import argparse
import ast
import os

parser = argparse.ArgumentParser()
parser.add_argument("--file_name", type=str, default='Logs/30-sysmon-more_20210818_1624.log', help="location of file to which the score will be calculated")
parser.add_argument("--save_to", type=str, default='Scores.txt', help="name of file where the score will be saved")
parser.add_argument("--correct_hit_score", type=int, default=5, help="positive score when player performs the task correctly")
parser.add_argument("--failed_hit_score", type=int, default=-1, help="negative score when player performs the task incorrectly")
opt = parser.parse_args()

# NOTE: opt.file_name should be a .log file
file = open(opt.file_name, "r")
# read content of file to string
data = file.read()
# The score is calculated based on the number of positive occurances, missed and wrong keyboard hits.
score = 0

# SYSMON task
# NOTE: if it's a communications task, then the following vars are 0
pos_occ = data.count("HIT")
missed = data.count("MISS")
wrong_occ = data.count("\tFA\n")
score += pos_occ*opt.correct_hit_score + (missed+wrong_occ) * opt.failed_hit_score

# COMMUNICATIONS task
st = 1
tmp = data

str_len1 = len("RADIOPROMPT\t")
str_len2 = len("TARGET\t")

while True:
    # Check if it's a communication file. If not, break
    st = tmp.find("RADIOPROMPT\t")
    if st == -1:
        break
    
    # Determine the frequency goal and if it's own or other's
    own = tmp[st+str_len1 : st+str_len1+3]
    target = tmp.find("TARGET\t")
    targetfreq = tmp[target+str_len2 : target+str_len2 + 5]
    name = tmp[target - 6: target - 1]
    expression = "\t" + name + "\t" + str(targetfreq)

    if "own" in own:
        if expression in data:
            # Add points when frequency changed correctly
            score += opt.correct_hit_score
        else:
            # If frequency changed incorrectly or didn't change
            score += opt.failed_hit_score
    elif "oth" in own:
        if "\t" + name + "\t1" in data:
            # Substract points if frequency changed
            score -= opt.correct_hit_score
    else:
        target = tmp.find("TARGET\t")
    
    tmp = tmp[target + str_len2:]


wr = str(score) + '\n'
if not os.path.exists(opt.save_to):
    with open(opt.save_to, 'w') as f:
        f.write(wr)
else:
    with open(opt.save_to, 'a') as f:
        f.write(wr)

