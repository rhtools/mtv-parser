from datetime import datetime
from datetime import timedelta
from collections import defaultdict

def extract_vm_information(entry) -> dict:
    """Calculate the total disk size for a migration plan."""
    total_disk_size = 0
    total_disk_transfer_time = timedelta(seconds=0)
    vm_information = {}
    for vm in entry["status"]["migration"]["vms"]:
        os_name = vm.get('operatingSystem')
        vm_name = vm.get('name')

        for phase in vm["pipeline"]:
            if phase["name"] == "DiskTransfer" and "progress" in phase and "total" in phase["progress"]:
                total_disk_size += phase["progress"]["total"]
                disk_transfer_start_time = datetime.fromisoformat(phase['started'])
                disk_transfer_end_time = datetime.fromisoformat(phase["completed"])
                total_disk_transfer_time = disk_transfer_end_time - disk_transfer_start_time
        vm_information.update({os_name: {'name': vm_name, 'disk_size': total_disk_size, 
                                         'transfer_time': total_disk_transfer_time.total_seconds() /60}})
    return vm_information

def analyze_concurrent_migrations(mtv_plan_data):
    # Create a list to store all VM migration events
    events = []
    
    for entry in mtv_plan_data["items"]:
        if "completed" in entry["status"]["migration"].keys():
            for vm in entry["status"]["migration"]["vms"]:
                os_type = vm.get('operatingSystem', 'unknown')
                vm_name = vm.get('name', 'unnamed')
                
                # Get VM-specific start and end times
                vm_start = datetime.fromisoformat(vm.get('started'))
                vm_end = datetime.fromisoformat(vm.get('completed'))
                
                # Add start and end events to the timeline
                events.append({"time": vm_start, "type": "start", "os": os_type, "name": vm_name})
                events.append({"time": vm_end, "type": "end", "os": os_type, "name": vm_name})
    
    # Sort events chronologically
    events.sort(key=lambda x: x["time"])
    
    # Track concurrent migrations
    concurrent_counts = defaultdict(int)
    max_concurrent = defaultdict(int)
    current_vms = defaultdict(list)
    timeline_data = []
    
    # Variables to track peak concurrency
    peak_time = None
    max_concurrent_total = 0
    concurrent_periods = []
    current_period = None
    
    # Process events in chronological order
    for event in events:
        os_type = event["os"]
        event_time = event["time"]
        
        if event["type"] == "start":
            concurrent_counts[os_type] += 1
            current_vms[os_type].append(event["name"])
        else:  # end event
            concurrent_counts[os_type] -= 1
            if event["name"] in current_vms[os_type]:
                current_vms[os_type].remove(event["name"])
        
        # Update maximum concurrency for this OS type
        max_concurrent[os_type] = max(max_concurrent[os_type], concurrent_counts[os_type])
        
        # Calculate total concurrent VMs across all OS types
        total_concurrent = sum(concurrent_counts.values())
        
        # Track periods of concurrency
        if current_period is None and total_concurrent > 0:
            # Start a new period
            current_period = {
                "start": event_time,
                "peak": total_concurrent,
                "peak_time": event_time
            }
        elif current_period is not None:
            if total_concurrent > current_period["peak"]:
                # Update peak within current period
                current_period["peak"] = total_concurrent
                current_period["peak_time"] = event_time
            elif total_concurrent == 0:
                # End the period
                current_period["end"] = event_time
                current_period["duration"] = (current_period["end"] - current_period["start"]).total_seconds() / 60  # minutes
                concurrent_periods.append(current_period)
                current_period = None
        
        # Update overall peak concurrency
        if total_concurrent > max_concurrent_total:
            max_concurrent_total = total_concurrent
            peak_time = event_time
        
        # Record the state at this point in time
        timeline_point = {
            "time": event_time,
            "concurrent_counts": dict(concurrent_counts),
            "current_vms": {k: list(v) for k, v in current_vms.items()},
            "total_concurrent": total_concurrent
        }
        timeline_data.append(timeline_point)
    
    # Close any open period at the end of processing
    if current_period is not None:
        current_period["end"] = events[-1]["time"]
        current_period["duration"] = (current_period["end"] - current_period["start"]).total_seconds() / 60  # minutes
        concurrent_periods.append(current_period)
    
    # Find significant drops in concurrency
    significant_drops = []
    drop_threshold = 0.5  # 50% drop
    
    for i in range(1, len(timeline_data)):
        prev_count = timeline_data[i-1]["total_concurrent"]
        curr_count = timeline_data[i]["total_concurrent"]
        
        if prev_count > 0 and curr_count < prev_count * (1 - drop_threshold):
            significant_drops.append({
                "time": timeline_data[i]["time"],
                "from": prev_count,
                "to": curr_count,
                "percentage": (prev_count - curr_count) / prev_count * 100
            })
    
    # Find time from peak to first significant drop
    time_to_drop = None
    if peak_time and significant_drops:
        for drop in significant_drops:
            if drop["time"] > peak_time:
                time_to_drop = (drop["time"] - peak_time).total_seconds() / 60  # minutes
                break
    
    return {
        "max_concurrent": dict(max_concurrent),
        "max_concurrent_total": max_concurrent_total,
        "peak_time": peak_time,
        "timeline": timeline_data,
        "concurrent_periods": concurrent_periods,
        "significant_drops": significant_drops,
        "time_to_significant_drop": time_to_drop
    }
