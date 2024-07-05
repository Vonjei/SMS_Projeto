import random
import math
import time

# Função para gerador congruente linear
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

# Função para obter os parâmetros do gerador congruente linear
def obter_parametros_congruente_linear():
    a = int(input("Digite o valor de 'a' para o gerador congruente linear (multiplicador): "))
    c = int(input("Digite o valor de 'c' para o gerador congruente linear (incremento): "))
    m = int(input("Digite o valor de 'm' para o gerador congruente linear (módulo): "))
    semente = int(input("Digite o valor da semente inicial para o gerador congruente linear (x0): "))
    return a, c, m, semente

# Função para simular chegadas de clientes
def simular_chegadas_clientes():
    def obter_media_clientes():
        return float(input("Informe a média de clientes por dia: "))

    modo = input("Deseja declarar a média de clientes por dia? (sim/não): ").strip().lower()
    if modo == 'sim':
        return obter_media_clientes(), None
    else:
        print("Opção inválida. Tente novamente.")
        return simular_chegadas_clientes()

# Função principal de simulação
def simular_dia(tempo_simulacao, tempo_medio_atendimento, media_clientes, a, c, m, semente, modo_simulacao):
    if media_clientes:
        taxa_chegada = 1 / media_clientes
        numero_eventos = int(media_clientes)
        numeros_aleatorios = gerar_numeros_congruentes_linear(a, c, m, semente, numero_eventos)
        tempos_chegada = [-math.log(1.0 - rn) / taxa_chegada for rn in numeros_aleatorios]
    else:
        print("Erro ao obter dados dos clientes.")
        return

    fila, tempos_saida = [], []
    comprimento_fila, tempo_total_ocupado, total_chegadas, total_partidas, tempo_atual = 0, 0, 0, 0, 0
    caixa = {'ocupado': False, 'proximo_tempo_saida': 0}

    tempos_espera = []

    for i, tempo_chegada in enumerate(tempos_chegada):
        total_chegadas += 1
        tempo_atual += tempo_chegada

        if modo_simulacao == 'tempo real':
            print(f"\nCliente {total_chegadas} entrou")
            time.sleep(random.uniform(0.5, 2.0))  # Pausa aleatória entre 0.5 e 2 segundos

        # Verifica se há caixa disponível
        if not caixa['ocupado']:
            caixa['ocupado'] = True
            tempo_atendimento = -math.log(1.0 - random.random()) * tempo_medio_atendimento
            caixa['proximo_tempo_saida'] = tempo_atual + tempo_atendimento
            tempos_saida.append(caixa['proximo_tempo_saida'])
            tempo_total_ocupado += tempo_atendimento
            total_partidas += 1

            if i > 0:
                tempos_espera.append(tempo_atual - sum(tempos_chegada[:i]))

            if modo_simulacao == 'tempo real':
                print(f"Caixa: Ocupado")
                print(f"Caixa realizou atendimento do Cliente {total_chegadas} em {tempo_atendimento:.2f} minutos")
                time.sleep(tempo_atendimento)  # Simula o tempo de atendimento

        else:
            fila.append(tempo_atual)
            comprimento_fila += 1

            if modo_simulacao == 'tempo real':
                print(f"Cliente {total_chegadas} foi ao caixa")
                print(f"Caixa: Ocupado, cliente entrou na fila")

        # Atendimento dos clientes na fila
        if caixa['ocupado'] and tempo_atual >= caixa['proximo_tempo_saida']:
            caixa['ocupado'] = False
            proximo_cliente = fila.pop(0)
            tempo_atendimento = -math.log(1.0 - random.random()) * tempo_medio_atendimento
            caixa['proximo_tempo_saida'] = tempo_atual + tempo_atendimento
            tempos_saida.append(caixa['proximo_tempo_saida'])
            tempo_total_ocupado += tempo_atendimento
            total_partidas += 1

            if i > 0:
                tempos_espera.append(tempo_atual - sum(tempos_chegada[:i]))

            caixa['ocupado'] = True

            if modo_simulacao == 'tempo real':
                print(f"\nCaixa: Ocupado")
                print(f"Caixa realizou atendimento do Cliente {total_chegadas - len(fila)} em {tempo_atendimento:.2f} minutos")
                time.sleep(random.uniform(1.0, 3.0))  # Pausa aleatória entre 1.0 e 3.0 segundos

    tempo_medio_espera = calcular_media(tempos_espera) if tempos_espera else 0
    media_comprimento_fila = comprimento_fila / numero_eventos if numero_eventos > 0 else 0
    ocupacao_servidor = tempo_total_ocupado / (tempo_simulacao)

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

    a, c, m, semente = obter_parametros_congruente_linear()

    media_clientes, _ = simular_chegadas_clientes()

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
