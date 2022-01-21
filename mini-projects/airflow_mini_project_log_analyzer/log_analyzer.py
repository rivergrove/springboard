from pathlib import Path

def analyze_file(log_dir):
    files = Path(log_dir).rglob('*.log')
    file_list = [x.as_posix() for x in files]
    
    log_list = []
    i = 0
    for file in file_list:
        with open(file, 'r') as fin:
            for line in fin:
                if 'ERROR - Failed to execute job' in line:
                    i += 1
                    log_list.append(line)
    return i, log_list