from dnslib.dns import RR, A
from dnslib.dns import CLASS, QTYPE
from dnslib import DNSRecord, DNSHeader, DNSQuestion
import socket

import sys

IP_VM = "192.168.100.119"
PUERTO_VM = 8000

root_ip = "198.41.0.4"

registro_cache = {}  #solo puede guardar 3 dominios , qname:(ip,cant)
historial_consultas_qname = [] #cuarda los ultimos 20 dominios consultados qname
historial_consultas_ip = []
#guarda una consulta en el historial y si es de las 3 mas buscadas en registro_cache

#hay un caso que hace q cambie todo pal informe
def guardarencache(nombre:str,ip:bytes):
    global historial_consultas_qname, historial_consultas_ip, registro_cache
    historial_consultas_qname.append(nombre)
    historial_consultas_ip.append(ip)
    if len(historial_consultas_qname) > 20:
        historial_consultas_qname = historial_consultas_qname[1:]
        historial_consultas_ip = historial_consultas_ip[1:]

    frecuencias = {}
    for nombre_ in historial_consultas_qname:
        if not nombre_ in frecuencias:
            frecuencias[nombre_] = 0
        frecuencias[nombre_] +=1

    maximos = []

    print(frecuencias)

    for i in range(min(3,len(frecuencias))):
        maximos.append(max(frecuencias,key=frecuencias.get))
        frecuencias.pop(maximos[-1])
    
    registro_cache.clear()

    for i in maximos:
        registro_cache[i] = historial_consultas_ip[historial_consultas_qname.index(i)]
    

def usarcache(qname):
    if qname in registro_cache:
        return registro_cache[qname]
    return None


debug = 0
def printg(text:str):
    if debug == 0 or debug == 2:
        print(text)
def printn(text:str):
    if debug == 1 or debug == 2:
        print(text)



def resolver(mensaje_consulta:bytes,ip_addr=root_ip) -> bytes:
    
    buff_size = 1024

    contador = 0

    while True:
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        contador+=1
        printn(f"Estuve {contador} aqui")
        address = (ip_addr,53)
        dns_aux = DNSRecord.parse(mensaje_consulta)
        name_con = dns_aux.q.get_qname()
        dns_socket.sendto(mensaje_consulta,address)

        response,address_response = dns_socket.recvfrom(buff_size)

        resp_dns = DNSRecord.parse(response)


        print([(QTYPE.get(x.rtype))+"   "+str(x.rdata) for x in resp_dns.rr])
        print([(QTYPE.get(x.rtype))+"   "+str(x.rdata) for x in resp_dns.ar])
        print([(QTYPE.get(x.rtype))+"   "+str(x.rdata) for x in resp_dns.auth])


        printn("Buscando tipo A")
        for t in resp_dns.rr:
            if QTYPE.get(t.rtype) == "A":
                printn("Encontrado, cerrando ciclo")
                dns_socket.close()
                return resp_dns.pack()
        printn("No encontrado tipo A")
        

        aux_NS = False
        for t in resp_dns.auth:
            aux_NS = aux_NS or (QTYPE.get(t.rtype) == "NS")

            
        if aux_NS:
            printn("Encontrado NS")

            tipos = [QTYPE.get(x.rtype) for x in resp_dns.ar]

            
            if "A" in tipos:
                tipo_a = tipos.index('A')
            else:
                tipo_a = -1
        
            if tipo_a != -1:
                ip_addr = str(resp_dns.ar[tipo_a].rdata)
                #mensaje_consulta = resp_dns.pack()
                printg(f"(debug) Consultando {name_con} a {resp_dns.ar[tipo_a ].rname} con dirección IP {resp_dns.ar[tipo_a ].rdata}")
                continue

            aux = False

            printn("No encontrado tipo A en AR")
            for t in resp_dns.auth:
                name_Server = t.rdata
                printg(f"(debug) Consultando {name_con} a {name_Server} con dirección IP {t.rdata}")
                printn(f"Entrando a recursion con: {name_Server}")
                dns_query = DNSRecord.question(qname=str(name_Server),qtype="A",qclass="IN")
                resp_rer = DNSRecord().parse(resolver(dns_query.pack()))
                if resp_rer != None:
                    printn("IP resuelta")
                    ip_addr = str(resp_rer.rr[0].rdata)
                    printg(f"(debug) Consultando {name_con} a {resp_rer.rr[0].rname} con dirección IP {resp_rer.rr[0].rdata}")
                    aux = True

            if aux:
                continue

        printn("No encontrado NS")
        
        break
    dns_socket.close()
    return resp_dns.pack()


if __name__ == "__main__":
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buff_size = 1024

    if len(sys.argv) > 1:
        if sys.argv[1] == "-g":
            debug = 1
        elif sys.argv[1] == "-t":
            debug = 2
        else:
            raise "Mijo pa que se enoja"

    printg("Entrando a debug")
    printn("NO estoy en debug")

    address_dns = (IP_VM,PUERTO_VM)

    dns_socket.bind(address_dns)

    while True:
        
        recv, address_resp = dns_socket.recvfrom(buff_size)
        dns = DNSRecord.parse(recv)

        qname = dns.q.get_qname()
        ip_a = usarcache(qname)

        if ip_a != None:
            printg(f"Resuelto por Cache: {qname}")
            
            resp = DNSRecord().parse(ip_a)
            resp.header.id = dns.header.id
            resp = resp.pack()
            

        else:
            resp = resolver(dns.pack())
            guardarencache(qname,resp)
        dns_socket.sendto(resp,address_resp)        

    dns_socket.close()