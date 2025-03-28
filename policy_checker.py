def check_policy(policy: dict, lla: dict, node_proof: dict):
    rules = policy.keys()
    
    for rule in rules:
        if policy[rule] != lla[rule]:
            print(f'Rule {rule} is incorrect, the proof is the node path {node_proof[rule]}')
    