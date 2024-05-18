# Importa as bibliotecas necessárias
import streamlit as st
import pandas as pd
import geopy
from geopy.distance import geodesic
import folium

# Cria uma função para adicionar manualmente os endereços
def add_manual_addresses():
    addresses = []
    num_addresses = 2  # Número inicial de linhas de inserção
    
    # Cria as linhas de inserção iniciais
    for i in range(num_addresses):
        address = st.text_input(f"Endereço {i+1}", placeholder="Digite um endereço")
        if address:
            addresses.append(address)
    
    # Cria o botão para adicionar mais linhas de inserção
    if st.button("Adicionar mais endereços"):
        num_addresses += 1
        address = st.text_input(f"Endereço {num_addresses}", placeholder="Digite um endereço")
        if address:
            addresses.append(address)
    
    return addresses

# Cria uma função para carregar os endereços de um arquivo CSV
def load_addresses_from_csv():
    uploaded_file = st.file_uploader("Carregar arquivo CSV")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        addresses = df["Endereço"].tolist()
        return addresses
    else:
        return []

# Cria uma função para obter a localização inicial e final
def get_start_and_end_locations():
    start_address = st.text_input("Endereço inicial", placeholder="Digite um endereço")
    end_address = st.text_input("Endereço final", placeholder="Digite um endereço")
    return start_address, end_address

# Cria uma função para gerar uma rota
def generate_route(addresses, start_address, end_address):
    # Converte os endereços em coordenadas geográficas
    geolocator = geopy.Nominatim(user_agent="streamlit-app")
    locations = [geolocator.geocode(address) for address in addresses]

    # Calcula a distância entre os locais
    distances = []
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            distance = geodesic(locations[i].latitude, locations[i].longitude,
                                locations[j].latitude, locations[j].longitude).km
            distances.append(distance)

    # Cria um grafo com os locais
    graph = {}
    for i in range(len(locations)):
        graph[i] = []
        for j in range(len(locations)):
            if i != j:
                graph[i].append((j, distances[i*len(locations) + j]))

    # Resolve o problema do caixeiro viajante usando o algoritmo Nearest Neighbor
    # Start node é o índice do endereço inicial
    start_node = [location for location in locations if location.address == start_address][0]
    visited = [start_node]
    path = [start_node]
    while len(visited) < len(locations):
        min_distance = float("inf")
        next_node = None
        for node in graph[visited[-1]]:
            if node not in visited and node[1] < min_distance:
                min_distance = node[1]
                next_node = node
        visited.append(next_node)
        path.append(next_node)
    
    # Imprime a rota otimizada
    route = [locations[start_node].address]
    for i in path:
        route.append(locations[i].address)
    st.write("### Rota otimizada:")
    st.write("\n".join(route))

    # Cria um mapa da rota
    map = folium.Map(location=[locations[start_node].latitude, locations[start_node].longitude], zoom_start=12)
    folium.PolyLine([[location.latitude, location.longitude] for location in locations], color="red").add_to(map)
    return map

# Cria a interface do usuário
st.title("Aplicativo de Otimização de Rotas")
st.markdown("### Digite os endereços ou carregue um arquivo CSV:")

# Esconde o botão de carregar CSV
st.markdown("""
<style>
#csv-file-uploader-container {
    display: none;
}
</style>
""", unsafe_allow_html=True)

option = st.selectbox("Adicionar endereços", ("Adicionar manualmente", "Carregar de CSV"))
if option == "Adicionar manualmente":
    addresses = add_manual_addresses()
elif option == "Carregar de CSV":
    # Mostra o botão de carregar CSV
    st.markdown("""
    <style>
    #csv-file-uploader-container {
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    addresses = load_addresses_from_csv()

start_address, end_address = get_start_and_end_locations()
if st.button("Gerar Rota"):
    map = generate_route(addresses, start_address, end_address)
    st.write(map)