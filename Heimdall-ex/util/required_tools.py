
required_tools = [
    # --- Network & Port Scanning ---
    ('nmap', 'nmap'),
    ('masscan', 'masscan'),

    # --- Web Enumeration ---
    ('gobuster', 'gobuster'),
    ('dirb', 'dirb'),
    ('nikto', 'nikto'),
    ('whatweb', 'whatweb'),
    ('feroxbuster', 'feroxbuster'),
    ('wfuzz', 'wfuzz'),

    # --- DNS Enumeration ---
    ('dnsrecon', 'dnsrecon'),
    ('dnsenum', 'dnsenum'),

    # --- SMB / Windows Enumeration ---
    ('enum4linux', 'enum4linux'),
    ('smbclient', 'smbclient'),
    ('smbmap', 'smbmap'),
    ('nbtscan', 'nbtscan-unixwiz'),

    # --- SNMP Enumeration ---
    ('snmpcheck', 'snmpcheck'),

    # --- General Utilities ---
    # ('ifconfig', 'net-tools'), # net-tools provides ifconfig, but 'ifconfig' is the command.
    ('whois', 'whois'),
    ('curl', 'curl'),
]