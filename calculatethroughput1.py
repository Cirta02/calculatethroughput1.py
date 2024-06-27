def extract_events(trace_file):
    events = []

    with open(trace_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 4:
                event_symbol = parts[0]
                event_time = float(parts[1])
                event_type = parts[2]
                event_details = " ".join(parts[3:])
                events.append((event_time, event_symbol, event_type, event_details))

    return events

def calculate_throughput(events):
    total_bytes = 0
    start_time = None
    end_time = None

    for event in events:
        event_time, event_symbol, event_type, event_details = event

        if event_symbol == '+' and "TxQueue/Enqueue" in event_type:
            if start_time is None:
                start_time = event_time
            size_str = event_details.split("Payload (size=")[1].split(")")[0]
            size = int(size_str)
            total_bytes += size

        elif event_symbol == '-' and "TxQueue/Dequeue" in event_type:
            end_time = event_time

    if start_time is not None and end_time is not None and end_time > start_time:
        duration = end_time - start_time
        throughput = (total_bytes * 8) / duration  # en bits par seconde
        print(f"Throughput: {throughput} bits/second")
    else:
        print("No valid events found for calculating throughput.")

def main():
    trace_file = "olsr-hna-csma.tr"
    events = extract_events(trace_file)
    print(f"Extracted {len(events)} events from trace file.")
    calculate_throughput(events)

if __name__ == "__main__":
    main()

