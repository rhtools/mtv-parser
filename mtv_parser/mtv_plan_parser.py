import yaml
from datetime import datetime, timedelta
from collections import defaultdict
from clioutput import CLIOutput
from vm_information import extract_vm_information, analyze_concurrent_migrations

def calculate_effective_migration_time(entry):
    """Calculate the effective migration time based on when the precopy duration drops significantly."""
    significant_drop_threshold = 0.5  # 50% drop

    # Find all precopies for this VM
    all_precopies = []
    for vm in entry["status"]["migration"]["vms"]:
        if "warm" in vm and "precopies" in vm["warm"]:
            for precopy in vm["warm"]["precopies"]:
                if "start" in precopy and "end" in precopy:
                    start_time = datetime.fromisoformat(precopy["start"])
                    end_time = datetime.fromisoformat(precopy["end"])
                    duration = (end_time - start_time).total_seconds() / 60  # Minutes
                    all_precopies.append({
                        "start": start_time,
                        "end": end_time,
                        "duration": duration
                    })
    
    # Sort precopies by start time
    all_precopies.sort(key=lambda x: x["start"])
    
    if not all_precopies:
        # Fallback to regular migration times if no precopies
        start = datetime.fromisoformat(entry["status"]["migration"]["started"])
        end = datetime.fromisoformat(entry["status"]["migration"]["completed"])
        return (end - start).total_seconds() / 60
    
    # Get the start time from the first precopy
    migration_start = all_precopies[0]["start"]
    
    # Get the initial duration
    initial_duration = all_precopies[0]["duration"]
    
    # Find when the precopy duration drops significantly
    migration_end = all_precopies[-1]["end"]  # Default to the last precopy
    
    for i in range(1, len(all_precopies)):
        current_duration = all_precopies[i]["duration"]
        
        # If we find a significant drop from the initial duration
        if current_duration < initial_duration * significant_drop_threshold:
            migration_end = all_precopies[i]["end"]
            break
    
    # Calculate effective migration time in minutes
    effective_minutes = (migration_end - migration_start).total_seconds() / 60
    
    return effective_minutes

def main():
    with open("examples/all_parma_mtv_plans.yaml", "r") as yaml_file:
        mtv_plan_data = yaml.safe_load(yaml_file)

    output = CLIOutput()
    successful_migrations = []
    failed_migrations = []
    all_vms = defaultdict(list)

    for entry in mtv_plan_data["items"]:
        if "completed" in entry["status"]["migration"].keys():
            # Calculate effective duration using the new function
            effective_duration = calculate_effective_migration_time(entry)
            
            # Calculate total disk size
            vm_information = extract_vm_information(entry)
            
            def add_vm(vm_information):
                dict_key = next(iter(vm_information.keys()))
                all_vms[dict_key].append({
                    'name': vm_information[dict_key]['name'],
                    'disk_size': vm_information[dict_key]['disk_size'],
                    'transfer_time': vm_information[dict_key]['transfer_time']
                })
            
            add_vm(vm_information)
            
            number_of_vms = len(entry["spec"]["vms"])
            vms_failed = False
            
            for vms in entry["status"]["migration"]["vms"]:
                for vm in vms["conditions"]:
                    if vm["type"] != "Succeeded":
                        vms_failed = True
            
            migration_dict = {
                "name": entry["metadata"]["name"],
                "total_duration_mins": effective_duration,
                "vms": number_of_vms,
                "vms_failed": f"{vms_failed}",
                "total_disk_size": next(iter(vm_information.values()))['disk_size']
            }
            
            if vms_failed:
                failed_migrations.append(migration_dict)
            else:
                successful_migrations.append(migration_dict)
    concurrency_data = analyze_concurrent_migrations(mtv_plan_data)
    print()
    output.write(output.migration_output(failed_migrations, "failed"))
    output.write(("\n\n"))
    output.write(output.migration_output(successful_migrations, "successful"))
    output.write(("\n\n"))
    output.write(output.operating_system_report(all_vms))
    output.write(("\n\n"))
    output.write(output.generate_concurrency_report(concurrency_data))
    output.close()


if __name__ == "__main__":
    main()
