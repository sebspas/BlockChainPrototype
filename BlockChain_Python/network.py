import json
import urllib


def register_new_nodes_on_destnode(newnode_adr, dest_node_adr, blockchain):
    data = {
        'nodes': [newnode_adr]
    }
    adr = dest_node_adr + '/nodes/register'
    send_data_to_node(adr, data, blockchain)


def send_data_to_node(dest_adr, data, blockchain):
    try:
        adr = dest_adr
        req = urllib.request.Request(adr)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req, jsondataasbytes)
    except urllib.error.URLError as e:
        print(f'Node at {dest_adr} not available, removing from address list')
        blockchain.remove_node_from_network(adr)
