
import tkinter as tk
from tkinter import ttk

class ProcessData:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completed = False

class CPUSchedulingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("800x600")

        self.processes = []
        self.algorithm = tk.StringVar()
        self.time_quantum = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Process input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        pid_label = tk.Label(input_frame, text="Process ID:")
        pid_label.grid(row=0, column=0)
        self.pid_entry = tk.Entry(input_frame)
        self.pid_entry.grid(row=0, column=1)

        arrival_time_label = tk.Label(input_frame, text="Arrival Time:")
        arrival_time_label.grid(row=0, column=2)
        self.arrival_time_entry = tk.Entry(input_frame)
        self.arrival_time_entry.grid(row=0, column=3)

        burst_time_label = tk.Label(input_frame, text="Burst Time:")
        burst_time_label.grid(row=0, column=4)
        self.burst_time_entry = tk.Entry(input_frame)
        self.burst_time_entry.grid(row=0, column=5)

        add_button = tk.Button(input_frame, text="Add Process", command=self.add_process)
        add_button.grid(row=0, column=6)

        # Algorithm selection frame
        algorithm_frame = tk.Frame(self.root)
        algorithm_frame.pack(pady=10)

        algorithm_label = tk.Label(algorithm_frame, text="Select Algorithm:")
        algorithm_label.grid(row=0, column=0)

        fcfs_radio = tk.Radiobutton(algorithm_frame, text="FCFS", variable=self.algorithm, value="FCFS")
        fcfs_radio.grid(row=0, column=1)

        sjf_radio = tk.Radiobutton(algorithm_frame, text="SJF", variable=self.algorithm, value="SJF")
        sjf_radio.grid(row=0, column=2)

        rr_radio = tk.Radiobutton(algorithm_frame, text="Round Robin", variable=self.algorithm, value="RR")
        rr_radio.grid(row=0, column=3)

        time_quantum_label = tk.Label(algorithm_frame, text="Time Quantum:")
        time_quantum_label.grid(row=0, column=4)
        self.time_quantum_entry = tk.Entry(algorithm_frame, textvariable=self.time_quantum)
        self.time_quantum_entry.grid(row=0, column=5)

        simulate_button = tk.Button(algorithm_frame, text="Simulate", command=self.simulate)
        simulate_button.grid(row=0, column=6)

        # Output frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10)

        output_label = tk.Label(output_frame, text="Output:")
        output_label.pack()

        self.output_text = tk.Text(output_frame, height=20, width=80)
        self.output_text.pack()

    def add_process(self):
        pid = self.pid_entry.get()
        arrival_time = int(self.arrival_time_entry.get())
        burst_time = int(self.burst_time_entry.get())

        process = ProcessData(pid, arrival_time, burst_time)
        self.processes.append(process)

        self.pid_entry.delete(0, tk.END)
        self.arrival_time_entry.delete(0, tk.END)
        self.burst_time_entry.delete(0, tk.END)

    def fcfs_scheduling(self):
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        output = []
        current_time = 0
        waiting_time = 0
        turnaround_time = 0

        for process in processes:
            if process.arrival_time > current_time:
                current_time = process.arrival_time
            waiting_time += current_time - process.arrival_time
            current_time += process.burst_time
            turnaround_time += current_time - process.arrival_time
            output.append(f"Process {process.pid} completed at time {current_time}")

        output.append(f"Average Waiting Time: {waiting_time / len(processes)}")
        output.append(f"Average Turnaround Time: {turnaround_time / len(processes)}")

        return "\n".join(output)

    def sjf_scheduling(self):
        processes = sorted(self.processes, key=lambda p: (p.burst_time, p.arrival_time))
        output = []
        current_time = 0
        waiting_time = 0
        turnaround_time = 0

        while processes:
            process = processes.pop(0)
            if process.arrival_time > current_time:
                current_time = process.arrival_time
            waiting_time += current_time - process.arrival_time
            current_time += process.burst_time
            turnaround_time += current_time - process.arrival_time
            output.append(f"Process {process.pid} completed at time {current_time}")

        output.append(f"Average Waiting Time: {waiting_time / len(self.processes)}")
        output.append(f"Average Turnaround Time: {turnaround_time / len(self.processes)}")

        return "\n".join(output)

    def rr_scheduling(self):
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        time_quantum = self.time_quantum.get()
        output = []
        current_time = 0
        waiting_time = 0
        turnaround_time = 0
        ready_queue = []

        while True:
            for process in processes:
                if process.arrival_time <= current_time and not process.completed:
                    ready_queue.append(process)

            if not ready_queue:
                break

            process = ready_queue.pop(0)
            if process.remaining_time <= time_quantum:
                current_time += process.remaining_time
                waiting_time += current_time - process.arrival_time - process.burst_time
                turnaround_time += current_time - process.arrival_time
                output.append(f"Process {process.pid} completed at time {current_time}")
                process.completed = True
            else:
                current_time += time_quantum
                process.remaining_time -= time_quantum
                ready_queue.append(process)

        output.append(f"Average Waiting Time: {waiting_time / len(self.processes)}")
        output.append(f"Average Turnaround Time: {turnaround_time / len(self.processes)}")

        return "\n".join(output)

    def simulate(self):
        algorithm = self.algorithm.get()
        if algorithm == "FCFS":
            result = self.fcfs_scheduling()
        elif algorithm == "SJF":
            result = self.sjf_scheduling()
        elif algorithm == "RR":
            result = self.rr_scheduling()
        else:
            result = "Please select an algorithm."

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

root = tk.Tk()
app = CPUSchedulingSimulator(root)
root.mainloop()
