import streamlit as st
from datetime import datetime, timedelta

st.title("Registro de ventas semanal 💰")

# FUNCIÓN para calcular fecha según el día
def obtener_fecha(dia):
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    hoy = datetime.now()
    indice_hoy = hoy.weekday()  # lunes=0
    
    indice_dia = dias.index(dia)
    
    diferencia = indice_dia - indice_hoy
    fecha = hoy + timedelta(days=diferencia)
    
    return fecha.strftime("%d-%m-%Y")

# Inicializar datos
if "ventas_semana" not in st.session_state:
    st.session_state.ventas_semana = {
        "lunes": {"ventas": []},
        "martes": {"ventas": []},
        "miercoles": {"ventas": []},
        "jueves": {"ventas": []},
        "viernes": {"ventas": []},
        "sabado": {"ventas": []},
        "domingo": {"ventas": []}
    }

ventas_semana = st.session_state.ventas_semana
dias = list(ventas_semana.keys())

# Seleccionar día
dia = st.selectbox("Selecciona el día", dias)

# Mostrar fecha automática
fecha_actual = obtener_fecha(dia)
st.write("📅 Fecha:", fecha_actual)

# FORMULARIO
with st.form("form_venta", clear_on_submit=True):
    producto = st.text_input("Producto")
    precio_texto = st.text_input("Precio")

    guardar = st.form_submit_button("Guardar venta 💾")

    if guardar:
        if producto != "" and precio_texto != "":
            try:
                precio = float(precio_texto)
                ventas_semana[dia]["ventas"].append((producto, precio))
                st.toast("Venta guardada ✔️")
            except:
                st.error("Precio inválido ❌")
        else:
            st.warning("Completa todos los campos ⚠️")

# Mostrar ventas del día
st.subheader(f"Ventas de {dia}")

total_dia = 0

for producto, precio in ventas_semana[dia]["ventas"]:
    st.write(f"{producto} - {precio} Bs")
    total_dia += precio

st.write(f"💰 Total del día: {total_dia} Bs")

# Resumen semanal
st.subheader("📊 Resumen semanal")

total_semana = 0
cantidad_total = 0

for d in dias:
    total_d = sum(precio for _, precio in ventas_semana[d]["ventas"])
    cantidad_d = len(ventas_semana[d]["ventas"])
    
    st.write(f"{d.capitalize()}: {cantidad_d} ventas | {total_d} Bs")
    
    total_semana += total_d
    cantidad_total += cantidad_d

# Inversión
inversion = st.number_input("💸 Inversión semanal", min_value=0.0)

ganancia = total_semana - inversion

st.write("🧾 Total vendido:", total_semana)
st.write("📦 Total de ventas:", cantidad_total)
st.write("💵 Ganancia:", ganancia)

# Resultado final
if ganancia > 0:
    st.success("Resultado: Hubo ganancia 💰")
elif ganancia == 0:
    st.info("Resultado: Se recuperó la inversión 🤝")
else:
    st.error("Resultado: Hubo pérdida ❌")