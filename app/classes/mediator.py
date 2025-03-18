import json


class Mediator():
    def __init__(self, bot, scanner):
        self.bot = bot
        self.scanner = scanner
        with open('conf.json', 'r') as file:
            config = json.load(file)
        self.hosts = config['hosts']

    def handle_request(self, request):
        if request == "status":
            self.bot.send_message("Ready to scan")
        if request == 'scan':
            self.handle_scan()
        if request == "settings":
            self.bot.send_message(
                f"Current hosts for scan:\n".join(
                    [f"{host['host_name']} ({host['host_ip']})" for host in self.hosts]))

    def handle_scan(self):
        collecting_message_response = self.bot.send_message(
            "Scan is running...")
        if collecting_message_response:
            collecting_message_id = collecting_message_response['result']['message_id']
        else:
            collecting_message_id = False
        try:
            scan_result = self.scanner.scan_hosts()
        except Exception as e:
            self.bot.send_message(
                f"Unknown error when scanning: {e}")
            return 1

        if collecting_message_id:
            self.bot.delete_message(collecting_message_id)
        try:
            report = self.format_scan_results(scan_result)
        except Exception as e:
            self.bot.send_message(f"Unknown error when creating report: {e}")
        self.bot.send_message(report)

    def format_scan_results(self, results):
        formatted_output = []
        for host in results:
            host_info = f"Host: {host['host_name']} ({host['host_ip']})\nState: {host['state']}"
            protocol_info = []
            for protocol in host['protocols']:
                ports_info = "\n".join(
                    [f"  Port: {port['port']}, State: {port['state']}" for port in protocol['ports']]
                )
                protocol_info.append(
                    f"Protocol: {protocol['protocol']}\n{ports_info}")
            host_details = f"{host_info}\n" + "\n".join(protocol_info)
            formatted_output.append(host_details)
        return "\n\n".join(formatted_output)
