import json
import nmap


class Scanner():

    def __init__(self):
        with open('conf.json', 'r') as file:
            config = json.load(file)
        self.hosts = config['hosts']
        self.nmap_args = config['nmap_arguments']
        self.port_range = config['port_range']

    def scan_hosts(self):
        result = []
        try:
            scanner = nmap.PortScanner()
            for host_note in self.hosts:
                scanner.scan(host_note['host_ip'],
                             self.port_range, arguments=self.nmap_args)

                host_result = {
                    'host_name': host_note['host_name'],
                    'host_ip': host_note['host_ip'],
                    'state': scanner[host_note['host_ip']].state(),
                    'protocols': []
                }

                for proto in scanner[host_note['host_ip']].all_protocols():
                    protocol_result = {
                        'protocol': proto,
                        'ports': []
                    }

                    ports = scanner[host_note['host_ip']][proto].keys()
                    for port in sorted(ports):
                        port_info = {
                            'port': port,
                            'state': scanner[host_note['host_ip']][proto][port]['state']
                        }
                        protocol_result['ports'].append(port_info)

                    host_result['protocols'].append(protocol_result)

                result.append(host_result)

        except Exception as e:
            raise Exception(e)

        return result

# [
#     {
#         'host_name': 'example_host',
#         'host_ip': '192.168.1.1',
#         'state': 'up',
#         'protocols': [
#             {
#                 'protocol': 'tcp',
#                 'ports': [
#                     {'port': 22, 'state': 'open'},
#                     {'port': 80, 'state': 'closed'}
#                 ]
#             },
#             {
#                 'protocol': 'udp',
#                 'ports': [
#                     {'port': 53, 'state': 'open'}
#                 ]
#             }
#         ]
#     },
#     {
#         'host_name': 'another_host',
#         'host_ip': '192.168.1.2',
#         'state': 'down',
#         'protocols': []
#     }
# ]
