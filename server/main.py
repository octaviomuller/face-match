import os
import face_recognition
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import platform
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import freeze_support
# import cupy as cp
import numpy as np
import pickle

CACHE_FILE = 'face_cache.pkl'
UPLOAD_FOLDER = '../alvo'
FACES_FOLDER = '../faces/'

app = Flask(__name__)
CORS(app)

def limpar_tela():
    os.system('clear' if platform.system() in ['Linux', 'Darwin'] else 'cls')

def carregar_imagem(arquivo_imagem):
    try:
        imagem = face_recognition.load_image_file(arquivo_imagem)
        codificacoes = face_recognition.face_encodings(imagem, model='cnn')
        if len(codificacoes) > 0:
            return arquivo_imagem, codificacoes[0]
    except Exception as e:
        print(f"Erro ao carregar imagem {arquivo_imagem}: {e}")
    return arquivo_imagem, None

def carregar_rostos(diretorio, num_workers, cache, names=None, moto=False, folders=None):
    lista_de_rostos = []
    
    names_lower = [name.lower() for name in names] if names else []
    
    def verifica_categoria(arquivo_txt):
        if not os.path.exists(arquivo_txt):
            return False
        with open(arquivo_txt, 'r') as f:
            conteudo = f.read()
            return (
                "CATEGORIA: A" in conteudo or
                "CNH Categoria: A" in conteudo or
                "CATEGORIA\t\tA" in conteudo
            )
        
    arquivos = []

    if folders:
        for folder in folders:
            subdir = os.path.join(diretorio, folder)
            if not os.path.exists(subdir):
                raise FileNotFoundError(f"A pasta '{subdir}' não existe.")
            if not os.listdir(subdir):
                raise ValueError(f"A pasta '{subdir}' está vazia.")
            
            arquivos.extend([
                os.path.join(subdir, f) for f in os.listdir(subdir) 
                if f.endswith((".jpg", ".png", ".jpeg")) and 
                (not names_lower or any(name in f.lower() for name in names_lower))
            ])
    else:
        # Caso contrário, procura arquivos diretamente no diretório
        arquivos = [
            os.path.join(diretorio, f) for f in os.listdir(diretorio) 
            if f.endswith((".jpg", ".png", ".jpeg")) and 
            (not names_lower or any(name in f.lower() for name in names_lower))
        ]
    
    if moto:
        arquivos = [f for f in arquivos if verifica_categoria(f"{os.path.splitext(f)[0]}.txt")]

    total_arquivos = len(arquivos)

    print(f"Total de arquivos para processar: {total_arquivos}")

    progresso_anterior = -1

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futuros = {}
        for arquivo in arquivos:
            if arquivo in cache:
                lista_de_rostos.append((arquivo, cache[arquivo]))
            else:
                futuros[executor.submit(carregar_imagem, arquivo)] = arquivo

        for i, futuro in enumerate(as_completed(futuros)):
            try:
                nome_arquivo, rosto = futuro.result()
                if rosto is not None:
                    lista_de_rostos.append((nome_arquivo, rosto))
                    cache[nome_arquivo] = rosto
                progresso = int((i + 1) / total_arquivos * 100)
                if progresso != progresso_anterior:
                    print(f"\rProgresso: {progresso}%", end='', flush=True)
                    progresso_anterior = progresso
            except Exception as e:
                print(f"Erro no futuro: {e}")

    print()
    return lista_de_rostos

def comparar_rostos(rosto_alvo, lista_de_rostos):
    print(rosto_alvo)
    print(lista_de_rostos)
    embeddings = np.array([rosto for _, rosto in lista_de_rostos]).astype(np.float32)
    rosto_alvo = np.array(rosto_alvo).astype(np.float32).reshape(1, -1)

    embeddings_gpu = cp.asarray(embeddings)
    rosto_alvo_gpu = cp.asarray(rosto_alvo)

    distancias = cp.linalg.norm(embeddings_gpu - rosto_alvo_gpu, axis=1)
    similaridades = (1 - distancias) * 100

    resultados = [(lista_de_rostos[i][0], similaridades[i].item()) for i in range(len(lista_de_rostos))]
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados

def comparar_rostos_api(caminho_imagem1, caminho_imagem2, api_url):
    print(f"Comparando {caminho_imagem1} com {caminho_imagem2}...", flush=True)
    try:
        with open(caminho_imagem1, 'rb') as img1, open(caminho_imagem2, 'rb') as img2:
            files = {'image_a': img1, 'image_b': img2}
            response = requests.post(api_url, files=files, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if "data" in result and "similarity" in result["data"]:
                    similarity_score = result["data"]["similarity"]
                    print(f"Pontuacao de Similaridade para {caminho_imagem1} e {caminho_imagem2}: {similarity_score}", flush=True)
                    return similarity_score
                else:
                    print(f"Nenhuma pontuacao de similaridade encontrada na resposta para {caminho_imagem1} e {caminho_imagem2}", flush=True)
                    print("Conteudo completo da resposta:", result, flush=True)
                    return None
            else:
                print(f"Falha ao obter resposta da API: {response.status_code}", flush=True)
                print("Conteudo da resposta:", response.content.decode(), flush=True)
                return None
    except Exception as e:
        print(f"Ocorreu uma excecao ao comparar {caminho_imagem1} e {caminho_imagem2}: {e}", flush=True)
        return None

def comparar_varios_rostos(target_image, filtered_images, api_url, gender):
    resultados = []
    print(f"Iniciando comparacao com a imagem alvo: {target_image}", flush=True)

    with ProcessPoolExecutor() as executor:
        future_to_pair = {executor.submit(comparar_rostos_api, target_image, image_path, api_url): (target_image, image_path) for image_path, _ in filtered_images}

        for future in as_completed(future_to_pair):
            image_path1, image_path2 = future_to_pair[future]
            try:
                similarity_score = future.result()
                resultados.append((image_path1, gender + '/' + os.path.basename(image_path2), similarity_score))
                print(f"Concluida a comparacao de {os.path.basename(image_path2)} com pontuacao {similarity_score}", flush=True)
            except Exception as exc:
                print(f"Ocorreu uma excecao: {exc}", flush=True)

    print(f"Comparacao concluida com a imagem alvo: {target_image}", flush=True)
    return resultados

def carregar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def salvar_cache(cache):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

@app.route('/', methods=['POST'])
def compare():
    freeze_support()
    limpar_tela()

    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    imagem_alvo = UPLOAD_FOLDER + '/' + file.filename

    num_workers = 7

    api_url = "https://api.facerecognition.io/api/v1/compare"

    names = request.form.getlist('names')
    folders = request.form.getlist('folders')
    gender = request.form.get('gender')
    moto = request.form.get('moto')

    if moto is not None:
        moto = bool(moto)
    
    if gender is None:
        gender = 'homens'
    else:
        gender = gender.lower()
    
    faces_folder = FACES_FOLDER + '/' + gender

    print("Iniciando comparacao local de rostos...", flush=True)
    rosto_alvo = carregar_imagem(imagem_alvo)[1]
    if rosto_alvo is None:
        print("Nao foi possivel carregar o rosto alvo.")
    else:
        print("Carregando rostos do diretorio...")
        cache = carregar_cache()
        lista_de_rostos = carregar_rostos(faces_folder, num_workers, cache, names, moto, folders)
        salvar_cache(cache)
        print("Rostos carregados, iniciando comparacao...")
        resultados_filtrados = comparar_rostos(rosto_alvo, lista_de_rostos)

        print("\nTop 10 resultados locais:")
        for nome_arquivo, similaridade in resultados_filtrados[:10]:
            print(f"{os.path.basename(nome_arquivo)} Similaridade: {similaridade:.2f}%", flush=True)

        melhores_resultados = resultados_filtrados[:100]

        if melhores_resultados:
            print("Iniciando comparacao de rostos pela API para os 100 melhores resultados...", flush=True)
            resultados = comparar_varios_rostos(imagem_alvo, melhores_resultados, api_url, gender)
            print("Script concluido.", flush=True)

            resultados_ordenados = sorted(resultados, key=lambda x: (x[2] is None, x[2]))

            limpar_tela()

            print("\nResultados ordenados da menor para a maior pontuacao de similaridade:")
            for target, face, score in resultados_ordenados:
                nome_face = os.path.basename(face)
                print(f"{nome_face} Similaridade: {score}%", flush=True)

            os.remove(imagem_alvo)
            return resultados_ordenados
        else:
            os.remove(imagem_alvo)
            print("Nenhum rosto encontrado.", flush=True)

@app.route('/faces/<path:filename>')
def serve_faces_files(filename):
    return send_from_directory(FACES_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
