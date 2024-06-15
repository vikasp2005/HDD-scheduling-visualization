import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def plot_and_save(disk_path, title):
    request_sequence = list(range(len(disk_path)))
    plt.figure(figsize=(10, 6))
    plt.plot(request_sequence, disk_path, marker='o', linestyle='-', color='b')
    plt.xticks(request_sequence)
    plt.yticks(sorted(set(disk_path)))
    plt.xlabel('Request Sequence')
    plt.ylabel('Cylinder Number')
    plt.title(title)
    plt.grid(True)
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def fcfs(initial_position, disk_requests):
    fcfs_order = disk_requests
    disk_path = [initial_position] + fcfs_order
    return disk_path

def sstf(initial_position, disk_requests):
    requests = disk_requests.copy()
    current_position = initial_position
    sequence = [current_position]
    
    while requests:
        closest_request = min(requests, key=lambda x: abs(x - current_position))
        sequence.append(closest_request)
        requests.remove(closest_request)
        current_position = closest_request
    
    return sequence

def scan(initial_position, disk_requests, max_disk):
    requests = sorted(disk_requests)
    sequence = [initial_position]
    if initial_position <= requests[0]:
        sequence.extend(requests)
    elif initial_position >= requests[-1]:
        sequence.extend(reversed(requests))
    else:
        upward_requests = [req for req in requests if req >= initial_position]
        downward_requests = [req for req in requests if req < initial_position]
        sequence.extend(upward_requests)
        sequence.append(max_disk)
        sequence.extend(reversed(downward_requests))
    
    return sequence

def cscan(initial_position, disk_requests, max_disk):
    requests = sorted(disk_requests)
    sequence = [initial_position]
    upward_requests = [req for req in requests if req >= initial_position]
    downward_requests = [req for req in requests if req < initial_position]
    sequence.extend(upward_requests)
    sequence.append(max_disk)
    sequence.extend(downward_requests)
    return sequence

def look(initial_position, disk_requests):
    requests = sorted(disk_requests)
    sequence = [initial_position]
    if initial_position <= requests[0]:
        sequence.extend(requests)
    elif initial_position >= requests[-1]:
        sequence.extend(reversed(requests))
    else:
        upward_requests = [req for req in requests if req >= initial_position]
        downward_requests = [req for req in requests if req < initial_position]
        sequence.extend(upward_requests)
        sequence.extend(reversed(downward_requests))
    return sequence

def clook(initial_position, disk_requests):
    requests = sorted(disk_requests)
    sequence = [initial_position]
    upward_requests = [req for req in requests if req >= initial_position]
    downward_requests = [req for req in requests if req < initial_position]
    sequence.extend(upward_requests)
    sequence.extend(downward_requests)
    return sequence

if __name__ == '__main__':
    method = sys.argv[1]
    initial_position = int(sys.argv[2])
    disk_requests = list(map(int, sys.argv[3].split(',')))
    max_disk = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None

    if method.upper() == 'FCFS':
        disk_path = fcfs(initial_position, disk_requests)
        title = 'FCFS Disk Scheduling Disk Movement'
    elif method.upper() == 'SSTF':
        disk_path = sstf(initial_position, disk_requests)
        title = 'SSTF Disk Scheduling Disk Movement'
    elif method.upper() == 'SCAN':
        disk_path = scan(initial_position, disk_requests, max_disk)
        title = 'SCAN Disk Scheduling Disk Movement'
    elif method.upper() == 'CSCAN':
        disk_path = cscan(initial_position, disk_requests, max_disk)
        title = 'C-SCAN Disk Scheduling Disk Movement'
    elif method.upper() == 'LOOK':
        disk_path = look(initial_position, disk_requests)
        title = 'LOOK Disk Scheduling Disk Movement'
    elif method.upper() == 'CLOOK':
        disk_path = clook(initial_position, disk_requests)
        title = 'C-LOOK Disk Scheduling Disk Movement'
    else:
        print("INVALID METHOD")
        sys.exit(1)

    total_head_movement = sum(abs(disk_path[i] - disk_path[i - 1]) for i in range(1, len(disk_path)))
    img_base64 = plot_and_save(disk_path, title)
    
    print(f"{total_head_movement}SPLIT_HERE{img_base64}")
