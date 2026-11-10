# este vai ser o arquivo com alguns códigos desenvolvidos em seleção e preparação que são úties e irei usar posteriormente.
# este NÃO É O ARQUIVO DA ENTREGA. Este código unica e simplesmente contêm helpers úteis. A entrega está em selecao_e_preparacao.ipynb

def buildDataset():
    from pathlib import Path
    from scipy.io import loadmat
    import numpy as np

    dados = Path("../../data")

    dataset = []

    for file in sorted(dados.rglob("*.mat")):
        data = loadmat(file, simplify_cells=True)

        nome = str(file.name)   # o nome do arquivo contêm as labels que eu quero pra montar o dataset

        nome = nome.split("_")
        nome[-1] = nome[-1].split(".")

        #print(nome)

        condition, severity, speed, channel, recording = None, None, None, None, None

        for i in range(len(nome)):
            if nome[0] == 'F0':
                condition = 0  
            elif nome[0] == 'F1':
                condition = 1
            elif nome[0] == 'F2':
                condition = 2
            elif nome[0] == 'F3':
                condition = 3

            if nome[1] == 'SV0':
                severity = 0
            elif nome[1] == 'SV1':
                severity = 1
            elif nome[1] == 'SV2':
                severity = 2
            elif nome[1] == 'SV3':
                severity = 3

            if nome[2] == 'SP0':
                speed = 0
            elif nome[2] == 'SP1':
                speed = 1
            elif nome[2] == 'SP2':
                speed = 2
            elif nome[2] == 'SP3':
                speed = 3

            if nome[3] == 'C1':
                channel = 1
            elif nome[3] == 'C2':
                channel = 2
            elif nome[3] == 'C3':
                channel = 3
            elif nome[3] == 'C4':
                channel = 4

            try:
                if nome[4][0] == 'R1':
                    recording = 1
                elif nome[4][0] == 'R2':
                    recording = 2
                elif nome[4][0] == 'R3':
                    recording = 3
            except:
                recording = 1

                if nome[3][0] == 'C1':
                    channel = 1
                elif nome[3][0] == 'C2':
                    channel = 2
                elif nome[3][0] == 'C3':
                    channel = 3
                elif nome[3][0] == 'C4':
                    channel = 4

        #checks de segurança:
        if condition is not None and severity is not None and speed is not None and channel is not None and recording is not None:
            pass
        else:
            print(f"dados inválidos em: {file.name}")
            #print(condition, severity, speed, channel, recording)
            continue

        acc = data['AccData']       #acelerômetro

        sampling_rate = acc['samplingRate']
        timestamps    = acc['t']
        signal        = acc['Vib_Data']

        data = [signal, sampling_rate, timestamps, condition, severity, speed, channel, recording]
        dataset.append(data)
    
    return dataset
        
def filterDataset(dataset, condition=None, severity=None, speed=None,
                  channel=None, recording=None):
    filtered_dataset = []

    for record in dataset:
        record_condition = record[3]
        record_severity = record[4]
        record_speed = record[5]
        record_channel = record[6]
        record_recording = record[7]

        matches = (
            (condition is None or record_condition == condition)
            and (severity is None or record_severity == severity)
            and (speed is None or record_speed == speed)
            and (channel is None or record_channel == channel)
            and (recording is None or record_recording == recording)
        )

        if matches:
            filtered_dataset.append(record)

    return filtered_dataset