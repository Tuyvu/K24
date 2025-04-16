from resolver import NameServer

def setup_dns_system():
    # Authoritative Servers
    auth_example = NameServer("auth_example", records={
        "www.example.com": "192.0.2.1",
        "mail.example.com": "192.0.2.2",
    })
    auth_test = NameServer("auth_test", records={
        "www.test.com": "198.51.100.1"
    })

    # TLD Servers
    tld_com = NameServer("tld_com", delegates={
        "example.com": auth_example,
        "test.com": auth_test,
    })

    # Root Server
    root = NameServer("root", delegates={
        "com": tld_com
    })

    return root