import shodan
import dns.resolver
import dns.message
import dns.query
import argparse

# ======================== CONFIG ========================
SHODAN_API_KEY = "UduWN5TASmISl0a9C0sa1aCOK3TvCnNL"
MAX_RESULTADOS = 40
# ========================================================

def buscar_dns_expuestos(api_key, query="port:53 country:CO", max_results=30):
    api = shodan.Shodan(api_key)
    resultados = []
    try:
        for resultado in api.search_cursor(query):
            ip = resultado.get('ip_str')
            org = resultado.get('org', 'Desconocida')
            pais = resultado.get('location', {}).get('country_name', 'Desconocido')
            if ip:
                resultados.append((ip, org, pais))
                if len(resultados) >= max_results:
                    break
    except shodan.APIError as e:
        print(f"[!] Error en Shodan: {e}")
    return resultados

def probar_resolucion(ip, dominio):
    mensaje = dns.message.make_query(dominio, dns.rdatatype.A)
    try:
        respuesta = dns.query.udp(mensaje, ip, timeout=3)
        if respuesta.answer:
            datos = [r.to_text() for r in respuesta.answer]
            return "UDP", datos
    except Exception:
        pass

    try:
        respuesta = dns.query.tcp(mensaje, ip, timeout=3)
        if respuesta.answer:
            datos = [r.to_text() for r in respuesta.answer]
            return "TCP", datos
    except Exception as e:
        return "ERROR", str(e)

    return "ERROR", "No se pudo resolver"

def verificar_recursividad(ip):
    consulta = dns.message.make_query("www.google.com", dns.rdatatype.A)
    try:
        respuesta = dns.query.udp(consulta, ip, timeout=3)
        if respuesta.answer:
            return True
    except Exception:
        pass
    return False

def modo_analisis(ip, dominios):
    print(f"\n[*] Analizando IP: {ip}")
    for dominio in dominios:
        estado, resultado = probar_resolucion(ip, dominio)
        print(f"  - Dominio: {dominio}")
        print(f"    Método: {estado}")
        print(f"    Respuesta: {resultado}")
    rec = verificar_recursividad(ip)
    print(f"    ¿Servidor recursivo?: {'Sí' if rec else 'No'}\n")

def modo_shodan(dominios):
    print("[*] Buscando servidores DNS públicos con Shodan...")
    resultados = buscar_dns_expuestos(SHODAN_API_KEY, max_results=MAX_RESULTADOS)
    for ip, org, pais in resultados:
        print(f"\n[+] IP: {ip}")
        print(f"    Organización: {org}")
        print(f"    País: {pais}")
        rec = verificar_recursividad(ip)
        print(f"    ¿Recursivo?: {'Sí' if rec else 'No'}")
        for dominio in dominios:
            estado, resultado = probar_resolucion(ip, dominio)
            print(f"    Dominio: {dominio} | Método: {estado} | Respuesta: {resultado}")

def aviso_legal():
    print("="*60)
    print("AVISO LEGAL:")
    print("Esta herramienta es solo para fines educativos y de auditoría autorizada.")
    print("El uso inadecuado puede ser ilegal. El autor no se hace responsable del uso indebido.")
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta de auditoría DNS (CLI)")
    parser.add_argument("-i", "--ip", help="IP específica para verificar")
    parser.add_argument("-d", "--dominios", required=True, help="Lista de dominios separados por comas")
    parser.add_argument("-s", "--shodan", action="store_true", help="Usar Shodan para buscar servidores DNS expuestos")

    args = parser.parse_args()
    aviso_legal()

    dominios = [d.strip() for d in args.dominios.split(",") if d.strip()]

    if args.shodan:
        modo_shodan(dominios)
    elif args.ip:
        modo_analisis(args.ip, dominios)
    else:
        print("[!] Debes especificar una IP (-i) o usar Shodan (-s). Usa -h para ayuda.")
