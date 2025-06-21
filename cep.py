# pip install streamlit requests pandas geopy
import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Configuração
st.set_page_config(page_title="Busca CEP Inteligente", page_icon="📍")
st.title("🌍 Busca de Endereço por CEP com Mapa Inteligente")

# Componentes UI
with st.expander("ℹ️ Como usar"):
    st.markdown("""
    1. Digite um CEP brasileiro (apenas números)
    2. O sistema buscará primeiro a cidade
    3. Depois tentará localizar o endereço exato
    4. Mostraremos o melhor resultado possível
    """)

cep_input = st.text_input("Digite o CEP (8 dígitos):", max_chars=8, placeholder="Ex: 01001000").strip()

# Inicializa o geocodificador
geolocator = Nominatim(user_agent="cep_app_v2")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def avaliar_qualidade_localizacao(location, cidade_esperada, uf_esperado):
    """Avalia se o resultado da geocodificação é confiável"""
    if not location:
        return False
    
    address = location.raw.get('address', {})
    cidade_encontrada = address.get('city', '').lower() or address.get('town', '').lower() or address.get('village', '').lower()
    estado_encontrado = address.get('state', '').lower()
    
    return (cidade_esperada.lower() in cidade_encontrada and 
            uf_esperado.lower() == estado_encontrado)

if cep_input and len(cep_input) == 8 and cep_input.isdigit():
    with st.spinner("Buscando informações..."):
        try:
            # Consulta ViaCEP
            viacep_url = f"https://viacep.com.br/ws/{cep_input}/json/"
            response = requests.get(viacep_url)
            dados_cep = response.json()

            if "erro" in dados_cep:
                st.error("CEP não encontrado")
            else:
                # Organiza dados
                cep_formatado = f"{cep_input[:5]}-{cep_input[5:]}"
                logradouro = dados_cep.get('logradouro', '')
                bairro = dados_cep.get('bairro', '')
                cidade = dados_cep.get('localidade', '')
                uf = dados_cep.get('uf', '')
                
                # 1. Primeira tentativa: Cidade + UF (garante pelo menos a cidade)
                location_cidade = geocode(f"{cidade}, {uf}, Brasil")
                
                # 2. Segunda tentativa: Endereço completo (se existir logradouro)
                location_exato = None
                if logradouro:
                    location_exato = geocode(f"{logradouro}, {bairro}, {cidade}, {uf}, Brasil")
                
                # Seleciona o melhor resultado
                best_location = None
                if location_exato and avaliar_qualidade_localizacao(location_exato, cidade, uf):
                    best_location = location_exato
                    precisao = "Endereço preciso"
                    zoom = 16
                elif location_cidade and avaliar_qualidade_localizacao(location_cidade, cidade, uf):
                    best_location = location_cidade
                    precisao = "Centro da cidade"
                    zoom = 12
                
                # Exibe resultados
                if best_location:
                    st.success("Localização encontrada!")
                    
                    # Layout em colunas
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("📋 Dados Completos")
                        st.markdown(f"""
                        - **CEP:** {cep_formatado}
                        - **Logradouro:** {logradouro or 'Não disponível'}
                        - **Bairro:** {bairro or 'Não disponível'}
                        - **Localidade:** {cidade}, {uf}
                        - **DDD:** {dados_cep.get('ddd', 'N/A')}
                        """)
                    
                    with col2:
                        st.subheader("📍 Coordenadas")
                        st.markdown(f"""
                        - **Latitude:** {best_location.latitude:.6f}
                        - **Longitude:** {best_location.longitude:.6f}
                        - **Precisão:** {precisao}
                        """)
                    
                    # Mapa
                    st.subheader("🗺️ Mapa de Localização")
                    st.caption(f"Mostrando: {precisao.lower()}")
                    
                    mapa_df = pd.DataFrame({
                        "lat": [best_location.latitude],
                        "lon": [best_location.longitude]
                    })
                    
                    st.map(mapa_df, zoom=zoom)
                    
                    # Debug (opcional)
                    with st.expander("Detalhes técnicos"):
                        st.write("Melhor resultado encontrado:", best_location)
                        st.json(best_location.raw)
                else:
                    st.warning("Localização não encontrada no mapa")
                    st.json(dados_cep)

        except Exception as e:
            st.error(f"Erro: {str(e)}")

# Rodapé
st.markdown("---")
st.caption("""
🔍 Dados de CEP: ViaCEP | Mapa: OpenStreetMap | 
Precisão variável conforme disponibilidade de dados
""")