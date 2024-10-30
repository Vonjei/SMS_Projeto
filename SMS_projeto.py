import random
import math
import time

# Função para gerar números usando o gerador congruente linear
def gerar_numeros_congruentes_linear(a, c, m, semente, tamanho):
    x = semente
    numeros = []
    for _ in range(tamanho):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros

# Função para calcular a média de uma lista
def calcular_media(lista):
    return sum(lista) / len(lista) if lista else 0

# Função para simular a chegada de clientes
def simular_chegadas_clientes(media_clientes):
    return media_clientes

# Função principal de simulação
def simular_dia(tempo_simulacao, tempo_medio_atendimento, media_clientes, a, c, m, semente, modo_simulacao):
    if media_clientes <= 0:
        print("Erro: Média de clientes deve ser maior que zero.")
        return

    taxa_chegada = 1 / media_clientes
    numero_eventos = int(media_clientes)
    numeros_aleatorios = gerar_numeros_congruentes_linear(a, c, m, semente, numero_eventos)
    tempos_chegada = [-math.log(1.0 - rn) / taxa_chegada for rn in numeros_aleatorios]

    total_chegadas = 0
    total_partidas = 0
    tempo_atual = 0
    fila = []
    caixa_ocupada = False
    proximo_tempo_saida = 0
    tempos_espera = []

    for tempo_chegada in tempos_chegada:
        total_chegadas += 1
        tempo_atual += tempo_chegada

        if modo_simulacao == 'tempo real':
            print(f"\nCliente {total_chegadas} entrou")
            time.sleep(random.uniform(0.5, 2.0))  # Pausa aleatória

        if not caixa_ocupada:
            caixa_ocupada = True
            tempo_atendimento = -math.log(1.0 - random.random()) * tempo_medio_atendimento
            proximo_tempo_saida = tempo_atual + tempo_atendimento

            if modo_simulacao == 'tempo real':
                print(f"Caixa: Ocupado, atendimento do Cliente {total_chegadas} em {tempo_atendimento:.2f} minutos")
                time.sleep(tempo_atendimento)  # Simula o tempo de atendimento
            total_partidas += 1
        else:
            fila.append(tempo_atual)  # Cliente entrou na fila
            if modo_simulacao == 'tempo real':
                print(f"Cliente {total_chegadas} foi ao caixa, mas está ocupado.")

        # Atendimento dos clientes na fila
        if caixa_ocupada and tempo_atual >= proximo_tempo_saida:
            caixa_ocupada = False
            if fila:  # Se há clientes na fila
                proximo_cliente = fila.pop(0)
                tempo_atendimento = -math.log(1.0 - random.random()) * tempo_medio_atendimento
                proximo_tempo_saida = tempo_atual + tempo_atendimento

                if modo_simulacao == 'tempo real':
                    print(f"Caixa: Ocupado, atendimento do próximo cliente em {tempo_atendimento:.2f} minutos")
                    time.sleep(tempo_atendimento)  # Simula o tempo de atendimento
                total_partidas += 1

    # Cálculo das estatísticas
    tempo_medio_espera = calcular_media(tempos_espera)
    media_comprimento_fila = len(fila) / total_chegadas if total_chegadas > 0 else 0
    ocupacao_servidor = total_partidas / tempo_simulacao

    return {
        'total_chegadas': total_chegadas,
        'total_partidas': total_partidas,
        'tempo_medio_espera': tempo_medio_espera,
        'media_comprimento_fila': media_comprimento_fila,
        'ocupacao_servidor': ocupacao_servidor
    }

def main():
    print("Simulação de Fila de Servidor Único")
    tempo_simulacao = float(input("Digite o tempo de simulação (em minutos): "))
    tempo_medio_atendimento = float(input("Digite o tempo médio de atendimento (em minutos): "))
    
    a = int(input("Digite o valor de 'a' (multiplicador): "))
    c = int(input("Digite o valor de 'c' (incremento): "))
    m = int(input("Digite o valor de 'm' (módulo): "))
    semente = int(input("Digite o valor da semente inicial (x0): "))
    
    media_clientes = float(input("Informe a média de clientes por dia: "))
    modo_simulacao = input("Deseja realizar a simulação em 'Tempo real' ou 'Rápida'? (tempo real/rápida): ").strip().lower()

    resultado = simular_dia(tempo_simulacao, tempo_medio_atendimento, media_clientes, a, c, m, semente, modo_simulacao)

    print("\nEstatísticas da simulação:")
    print(f'Total de chegadas: {resultado["total_chegadas"]}')
    print(f'Total de partidas: {resultado["total_partidas"]}')
    print(f'Tempo médio de espera: {resultado["tempo_medio_espera"]:.2f} minutos')
    print(f'Média do comprimento da fila: {resultado["media_comprimento_fila"]:.2f}')
    print(f'Ocupação do servidor: {resultado["ocupacao_servidor"]:.2f}')

if __name__ == "__main__":
    main()
