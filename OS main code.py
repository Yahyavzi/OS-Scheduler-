import random

def poisson_random(lmbda):
    # Generates a Poisson-distributed random number using the Knuth algorithm
    L = pow(2.718281828459045, -lmbda)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def generate_processes(num_processes, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda):
    processes = []
    for pid in range(1, num_processes + 1):
        arrival_time = max(0, int(random.gauss(arrival_mean, arrival_std)))
        burst_time = max(1, int(random.gauss(burst_mean, burst_std)))
        priority = poisson_random(priority_lambda)
        processes.append((f'P{pid}', arrival_time, burst_time, priority))

    processes.sort(key=lambda x: x[1])  # Sort by arrival_time
    return processes

def save_to_file(processes, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{len(processes)}\n")
        f.write("process_id arrival_time burst_time priority\n")
        for p in processes:
            f.write(f"{p[0]} {p[1]} {p[2]} {p[3]}\n")

def main():
    input_file = "input.txt"
    output_file = "processes.txt"

    with open(input_file, 'r') as f:
        lines = f.readlines()

    num_processes = int(lines[0].strip())
    arrival_mean, arrival_std = map(float, lines[1].strip().split())
    burst_mean, burst_std = map(float, lines[2].strip().split())
    priority_lambda = float(lines[3].strip())

    processes = generate_processes(num_processes, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda)
    save_to_file(processes, output_file)

    print(f"[+] {len(processes)} processes generated and saved to '{output_file}'.")

if __name__ == "__main__":
    main()