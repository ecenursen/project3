from HappyCoinNode import HappyCoinNode

current_IP2 = "192.168.1.3"   
current_IP = ''
available_ports = [12000,3000,4000]    
current_port = 4000   

node1 = HappyCoinNode(current_IP2,available_ports[0])
node2 = HappyCoinNode(current_IP2,available_ports[1])
node3 = HappyCoinNode(current_IP2,available_ports[2])

print("nodes created")

node1.start()
node2.start()
node3.start()


node1.connect_to_node(current_IP2,available_ports[1])
node1.connect_to_node(current_IP2,available_ports[2])
node3.connect_to_node(current_IP2,available_ports[1])

node1.send_to_nodes({"a":12})
node2.send_to_nodes({"b":23})
node3.send_to_nodes({"c":34})

node1.stop()
node2.stop()
node3.stop()