import shodan
import dns.resolver
import dns.message
import dns.query
import csv
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ======================== CONFIG ========================
SHODAN_API_KEY = "UduWN5TASmISl0a9C0sa1aCOK3TvCnNL"
MAX_RESULTADOS = 40
RESULTADOS_POR_PAGINA = 10
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
        return resultados
    except shodan.APIError as e:
        messagebox.showerror("Error de Shodan", str(e))
        return []

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

def mostrar_pagina():
    for row in tree.get_children():
        tree.delete(row)
    start = pagina_actual * RESULTADOS_POR_PAGINA
    end = start + RESULTADOS_POR_PAGINA
    for datos in datos_filtrados[start:end]:
        tree.insert("", "end", values=datos)

def siguiente_pagina():
    global pagina_actual
    if (pagina_actual + 1) * RESULTADOS_POR_PAGINA < len(datos_filtrados):
        pagina_actual += 1
        mostrar_pagina()

def pagina_anterior():
    global pagina_actual
    if pagina_actual > 0:
        pagina_actual -= 1
        mostrar_pagina()

def buscar_y_mostrar():
    global datos_filtrados, pagina_actual

    dominios_texto = entry_dominio.get().strip()
    if not dominios_texto:
        messagebox.showwarning("Dominio requerido", "Debes ingresar al menos un dominio separado por comas.")
        return

    lista_dominios = [d.strip() for d in dominios_texto.split(",") if d.strip()]
    resultados = buscar_dns_expuestos(SHODAN_API_KEY, max_results=MAX_RESULTADOS)

    datos_filtrados = []
    for ip, org, pais in resultados:
        recursivo = verificar_recursividad(ip)
        for dominio in lista_dominios:
            estado, resultado = probar_resolucion(ip, dominio)
            datos_filtrados.append((ip, org, pais, dominio, estado, resultado, "Sí" if recursivo else "No"))

    pagina_actual = 0
    mostrar_pagina()

def verificar_ip():
    ip = entry_ip.get().strip()
    dominios_texto = entry_dominio.get().strip()
    if not ip or not dominios_texto:
        messagebox.showwarning("Faltan datos", "Debes ingresar una IP y al menos un dominio.")
        return

    lista_dominios = [d.strip() for d in dominios_texto.split(",") if d.strip()]
    resultados = []
    for dominio in lista_dominios:
        estado, resultado = probar_resolucion(ip, dominio)
        resultados.append(f"{dominio} => {estado}: {resultado}")

    messagebox.showinfo("Resultado", f"{ip} resolvi\u00f3:\n\n" + "\n".join(resultados))

def al_hacer_doble_click(event):
    item = tree.selection()
    if item:
        valores = tree.item(item, "values")
        ip = valores[0]
        dominio = valores[3]
        estado, resultado = probar_resolucion(ip, dominio)
        messagebox.showinfo("Resoluci\u00f3n directa", f"{ip} resolvi\u00f3 {dominio}:\n{resultado}")

# ===================== GUI =====================
root = tk.Tk()
root.title("Auditor\u00eda DNS con Shodan")

# Aviso legal
messagebox.showinfo(
    "Aviso Legal",
    "Esta herramienta es solo para fines educativos y de auditor\u00eda autorizada. "
    "El uso inadecuado puede ser ilegal. El autor no se hace responsable del uso indebido."
)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

entry_ip = ttk.Entry(frame, width=20)
entry_ip.grid(row=0, column=1)
entry_dominio = ttk.Entry(frame, width=50)
entry_dominio.grid(row=1, column=1)

btn_verificar = ttk.Button(frame, text="Verificar IP", command=verificar_ip)
btn_verificar.grid(row=0, column=2, padx=5)

btn_buscar = ttk.Button(frame, text="Buscar DNS Expuestos", command=buscar_y_mostrar)
btn_buscar.grid(row=2, column=1, pady=5)

# Etiquetas
ttk.Label(frame, text="IP a verificar:").grid(row=0, column=0, sticky="w")
ttk.Label(frame, text="Dominios (separados por comas):").grid(row=1, column=0, sticky="w")

# Tabla de resultados
columnas = ("IP", "Organizaci\u00f3n", "Pa\u00eds", "Dominio", "M\u00e9todo", "Respuesta", "\u00bfRecursivo?")
tree = ttk.Treeview(root, columns=columnas, show="headings")
for col in columnas:
    tree.heading(col, text=col)
    tree.column(col, width=140 if col != "Respuesta" else 300)

tree.pack(fill="both", expand=True)
tree.bind("<Double-1>", al_hacer_doble_click)

# Controles de paginaci\u00f3n
frame_pag = ttk.Frame(root)
frame_pag.pack(pady=5)
ttk.Button(frame_pag, text="Anterior", command=pagina_anterior).pack(side="left", padx=10)
ttk.Button(frame_pag, text="Siguiente", command=siguiente_pagina).pack(side="left", padx=10)

# Variables globales
datos_filtrados = []
pagina_actual = 0

root.mainloop()
