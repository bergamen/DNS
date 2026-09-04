from dnslib import DNSRecord

class DNS:
    def __init__(self):
        self.Qname = ""
        self.ANCOUNT = ""
        self.NSCOUNT = ""
        self.ARCOUNT = ""
        self.Answer = ""
        self.Authority = ""
        self.Additional = ""
    # def parse(self,hex_code:str):
        
    #     self.ANCOUNT = hex_code[12:16]
    #     self.ARCOUNT = hex_code[16:20]
    #     self.NSCOUNT = hex_code[20:24]
    #     hex_code = hex_code[:24]
    #     index = hex_code.find("00")
    #     self.Qname = hex_code[:index+2]
    #     hex_code = hex_code[:index+10]
    #     self.Answer = hex_code[:8*4]
    
    def parse(self,dns:DNSRecord):
        self.Qname = str(dns.q).split(" ")[0].strip(";")
        dns.rr.

    






        