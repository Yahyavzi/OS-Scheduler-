import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
import heapq

# --- Load Process Data ---
def load_processes(file_path):
    processes = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[2:]
        for line in lines:
            parts = line.strip().split()
            pid = parts[0]
            arrival = int(parts[1])
            burst = int(parts[2])
            priority = int(parts[3])
            processes.append({'pid': pid, 'arrival': arrival, 'burst': burst, 'priority': priority})
    return processes

# --- Scheduling Algorithms ---
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x['arrival'])
    time, result = 0, []
    for p in processes:
        start = max(time, p['arrival'])
        finish = start + p['burst']
        result.append((p['pid'], p['arrival'], p['burst'], start, finish, start - p['arrival'], finish - p['arrival']))
        time = finish
    return result

def priority_scheduling(processes):
    processes.sort(key=lambda x: (x['arrival'], -x['priority']))
    ready_queue, time, result = [], 0, []
    while processes or ready_queue:
        while processes and processes[0]['arrival'] <= time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: -x['priority'])
            p = ready_queue.pop(0)
            start = max(time, p['arrival'])
            finish = start + p['burst']
            result.append((p['pid'], p['arrival'], p['burst'], start, finish, start - p['arrival'], finish - p['arrival']))
            time = finish
        else:
            time += 1
    return result

def round_robin_scheduling(processes, quantum):
    processes.sort(key=lambda x: x['arrival'])
    queue, time, i = deque(), 0, 0
    rem = {p['pid']: p['burst'] for p in processes}
    start, finish, wait, turn = {}, {}, {}, {}
    result = []

    while i < len(processes) or queue:
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i])
            i += 1
        if queue:
            p = queue.popleft()
            pid = p['pid']
            if pid not in start:
                start[pid] = time
            t = min(quantum, rem[pid])
            time += t
            rem[pid] -= t
            while i < len(processes) and processes[i]['arrival'] <= time:
                queue.append(processes[i])
                i += 1
            if rem[pid] > 0:
                queue.append(p)
            else:
                finish[pid] = time
                turn[pid] = finish[pid] - p['arrival']
                wait[pid] = turn[pid] - p['burst']
                result.append((pid, p['arrival'], p['burst'], start[pid], finish[pid], wait[pid], turn[pid]))
        else:
            time += 1
    return result

def srtf_scheduling(processes):
    n = len(processes)
    processes.sort(key=lambda x: x['arrival'])
    remaining = {p['pid']: p['burst'] for p in processes}
    arrived, time, i, complete = [], 0, 0, 0
    start, finish = {}, {}
    result = []

    while complete < n:
        while i < n and processes[i]['arrival'] <= time:
            p = processes[i]
            heapq.heappush(arrived, (remaining[p['pid']], p['arrival'], p['pid'], p))
            i += 1
        if arrived:
            rem, arr, pid, p = heapq.heappop(arrived)
            if pid not in start:
                start[pid] = time
            remaining[pid] -= 1
            time += 1
            if remaining[pid] > 0:
                heapq.heappush(arrived, (remaining[pid], arr, pid, p))
            else:
                finish[pid] = time
                result.append((pid, p['arrival'], p['burst'], start[pid], finish[pid],
                               start[pid] - p['arrival'], finish[pid] - p['arrival']))
                complete += 1
        else:
            time += 1
    return result

# --- Result Table Display ---
def show_results(results, title):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("800x400")
    win.configure(bg='#1f1f2e')

    title_label = tk.Label(win, text=title, font=("Segoe UI", 18, "bold"), fg='white', bg='#1f1f2e')
    title_label.pack(pady=10)

    cols = ["PID", "Arrival", "Burst", "Start", "Finish", "Waiting", "Turnaround"]
    tree = ttk.Treeview(win, columns=cols, show='headings', height=15)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)
    for row in results:
        tree.insert("", tk.END, values=row)
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# --- Execute Algorithm ---
def run_scheduler(algo):
    try:
        data = load_processes("processes.txt")
        if algo == "FCFS":
            result = fcfs_scheduling(data)
        elif algo == "Priority":
            result = priority_scheduling(data)
        elif algo == "RR":
            result = round_robin_scheduling(data, quantum=2)
        elif algo == "SRTF":
            result = srtf_scheduling(data)
        else:
            raise ValueError("Unknown algorithm")
        show_results(result, f"{algo} Scheduling")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Layout ---
app = tk.Tk()
app.title("OS Scheduler")
app.geometry("850x500")
app.configure(bg="#f0f2f5")

# Sidebar
sidebar = tk.Frame(app, bg="#0f172a", width=200)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(sidebar, text="Schedulers", bg="#0f172a", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=20)

buttons = [("First Come First Serve", "FCFS"),
           ("Priority Scheduling", "Priority"),
           ("Round Robin", "RR"),
           ("SRTF", "SRTF")]

for text, key in buttons:
    btn = tk.Button(sidebar, text=text, command=lambda k=key: run_scheduler(k),
                    bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"),
                    activebackground="#1e40af", padx=10, pady=5, bd=0)
    btn.pack(pady=10, fill=tk.X, padx=20)

# Main Area
main_label = tk.Label(app, text="Welcome to OS Scheduler", font=("Segoe UI", 22, "bold"), bg="#f0f2f5", fg="#111827")
main_label.pack(pady=50)

sub_text = tk.Label(app, text="Select a scheduling algorithm from the left sidebar to visualize results.",
                    font=("Segoe UI", 12), bg="#f0f2f5", fg="#374151")
sub_text.pack()

app.mainloop()