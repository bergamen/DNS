from dnslib.dns import QTYPE
from dnslib import DNSRecord, RR , A
import socket

import sys

IP_VM = "192.168.100.119"
PUERTO_VM = 8000

buff_size = 1024

root_ip = (".","198.41.0.4")
deb = 0
cache = 0

historial_consultas = []

registro_cache = {}

def save_cache(nombre:str,ip:str):

    global registro_cache,historial_consultas

    if cache == 0:
        return

    historial_consultas.append(nombre)

    if nombre in registro_cache or len(registro_cache) < 3:
        registro_cache[nombre] = ip


    if len(historial_consultas) > 20:
        historial_consultas = historial_consultas[1:]


    min_ip = min(registro_cache,key=registro_cache.get)

    sum_min = sum([x==min_ip for x in historial_consultas])

    aux_consultas = historial_consultas.copy()

    for name in registro_cache:
        while name in aux_consultas:
            aux_consultas.remove(name)

    max_name = ""
    cant_name = 0
    while len(aux_consultas) > 0:
        primero = aux_consultas[0]
        cantidad_aux = sum([x==primero for x in aux_consultas])
        if cantidad_aux > cant_name:
            cant_name = cantidad_aux
            max_name = primero
        while primero in aux_consultas:
            aux_consultas.remove(primero)

    if cant_name > sum_min:
        registro_cache.pop(min_ip)
        registro_cache[max_name] = None

        if max_name == name:
            registro_cache[max_name] = ip
    

def use_cache(qname):
    if cache == 0:
        return None
    
    if qname in registro_cache:
        if deb == 1:
            print(f"(debug) {qname} resuelta por cache: {registro_cache[qname]}")
        return registro_cache[qname]
    return None




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

            name_Server = str(ns_rr.rdata)
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
        if "g" in sys.argv[1]:
            deb = 1
        if "c" in sys.argv[1]:
            cache = 1


    address_dns = (IP_VM,PUERTO_VM)

    dns_socket.bind(address_dns)

    while True:
        
        recv, address_resp = dns_socket.recvfrom(buff_size)
        dns = DNSRecord.parse(recv)

        qname = dns.q.get_qname()
        ip_a = use_cache(qname)

        if ip_a != None:
            dns.add_answer(RR(qname,QTYPE.A,rdata=A(ip_a)))
            resp = dns.pack()
            save_cache(qname,ip_a)
            
        else:
            resp = resolver(dns.pack())

            dns_aux = DNSRecord.parse(resp)
            new_ip = None
            for i in dns_aux.rr:
                if QTYPE.get(i.rtype) == "A":
                    new_ip = i
            if new_ip != None:
                save_cache(qname,str(i.rdata))
        dns_socket.sendto(resp,address_resp)        

    dns_socket.close()