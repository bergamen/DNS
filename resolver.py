from dnslib.dns import QTYPE
from dnslib import DNSRecord
import socket

import sys

IP_VM = "192.168.100.119"
PUERTO_VM = 8000

buff_size = 1024

root_ip = (".","198.41.0.4")

historial_consultas = [] 

registro_cache = {} 
historial_name = {} #guardas las 17 menos usadas
historial_ip = {} 

def save_cache(nombre:str,ip:bytes):

    global registro_cache,historial_name,historial_ip,historial_consultas

    historial_consultas.append(nombre)
    if not nombre in historial_name and not nombre in registro_cache:
        historial_name[nombre] = 1

        parse_cache = DNSRecord().parse(ip)

        historial_ip[nombre] = (parse_cache.rr,parse_cache.ar,parse_cache.auth)
    elif nombre in historial_name:
        historial_name[nombre] += 1
    elif nombre in registro_cache:
        registro_cache[nombre] += 1

    if len(historial_consultas) > 20:
        last_name = historial_consultas[0]
        historial_consultas = historial_consultas[1:]

        if last_name in historial_name:

            historial_name[last_name] -= 1

            if historial_name[last_name] == 0:
                historial_name.pop(last_name)
                historial_ip.pop(last_name)

        elif last_name in registro_cache:
            registro_cache[last_name] -= 1
            
            if registro_cache[last_name] == 0:
                registro_cache.pop(last_name)
                registro_cache.pop(last_name)

    if len(registro_cache) < 3 and len(historial_name) > 0:
        max_ip = max(historial_name,key=historial_name.get)
        registro_cache[max_ip] = historial_name[max_ip]
        historial_name.pop(max_ip)
    elif len(historial_name) > 0:
        max_ip = max(historial_name,key=historial_name.get)
        min_ip = min(registro_cache,key=registro_cache.get)
        if historial_name[max_ip] > registro_cache[min_ip]:
            historial_name[min_ip] = registro_cache[min_ip]
            registro_cache[max_ip] = historial_name[max_ip]
            registro_cache.pop(min_ip)
            historial_name.pop(max_ip)
    

def use_cache(qname):
    if deb == 1:
        print("IP resuelta por cache")
    
    if qname in registro_cache:
        return historial_ip[qname]
    return None


deb = 0

def debug(qname,ns,ip):
    if deb == 1:
        print(f"(debug) Consultando {qname} a {ns} con dirección IP {ip}")


def resolver(mensaje_consulta:bytes,ip_addr=root_ip) -> bytes:
    while True:
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (ip_addr[1],53)

        qname = DNSRecord().parse(mensaje_consulta).q.qname

        debug(qname,ip_addr[0],ip_addr[1])
        dns_socket.sendto(mensaje_consulta,address)

        response, _ = dns_socket.recvfrom(buff_size)

        resp_dns = DNSRecord.parse(response)

        for rr in resp_dns.rr:
            if QTYPE.get(rr.rtype) == "A":
                dns_socket.close()
                return resp_dns.pack()
        

        ns_rr = None
        for rr in resp_dns.auth:
            if QTYPE.get(rr.rtype) == "NS":
                ns_rr = rr

            
        if ns_rr != None:

            ar_rr = None
            for rr in resp_dns.ar:
                if QTYPE.get(rr.rtype) == "A":
                    ar_rr = rr
                    break

            if ar_rr != None:
                ip_addr = (ar_rr.rname,str(ar_rr.rdata))
                dns_socket.close()
                continue

            name_Server = ns_rr.rdata
            dns_query = DNSRecord.question(qname=name_Server,qtype="A",qclass="IN")
            resp_rer = DNSRecord().parse(resolver(dns_query.pack()))

            ip_addr = (resp_rer.rr[0].rname,str(resp_rer.rr[0].rdata))
            dns_socket.close()
            continue
        
        break
    dns_socket.close()
    return resp_dns.pack()


if __name__ == "__main__":
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buff_size = 1024

    if len(sys.argv) > 1:
        if sys.argv[1] == "-g":
            deb = 1
        else:
            raise "Error: Argumento innecesario"


    address_dns = (IP_VM,PUERTO_VM)

    dns_socket.bind(address_dns)

    while True:
        
        recv, address_resp = dns_socket.recvfrom(buff_size)
        dns = DNSRecord.parse(recv)

        qname = dns.q.get_qname()
        ip_a = use_cache(qname)

        if ip_a != None:
            dns.rr = ip_a[0]
            dns.ar = ip_a[1]
            dns.auth = ip_a[2]
            resp = dns.pack()
            save_cache(qname,resp)
            
        else:
            resp = resolver(dns.pack())
            save_cache(qname,resp)
        dns_socket.sendto(resp,address_resp)        

    dns_socket.close()