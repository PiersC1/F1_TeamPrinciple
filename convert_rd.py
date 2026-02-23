import json

def convert_tree():
    with open("src/database/rd_tree.json", "r") as f:
        data = json.load(f)
        
    for node in data:
        # Cost was usually in the millions (e.g. 5000000). Let's convert to an RP scale (e.g. 500)
        old_cost = node.pop("cost")
        node["rp_cost"] = int(old_cost / 10000)
        
        # Time was in 'Races' (e.g. 4). Let's convert to Total Engineer Workload.
        # Assume a standard pool of 50 engineers. So 4 races = 200 workload.
        old_time = node.pop("time_to_complete")
        node["base_workload"] = old_time * 50
        
    with open("src/database/rd_tree.json", "w") as f:
        json.dump(data, f, indent=4)
        print("Converted rd_tree.json successfully.")

if __name__ == "__main__":
    convert_tree()
