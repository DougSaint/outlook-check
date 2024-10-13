def filtrar_sucesso_ig(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
        
        # Filtra as linhas que terminam com "IG : Y"
        linhas_filtradas = [linha for linha in linhas if linha.strip().endswith("IG : Y")]
        
        # Escreve as linhas filtradas em um novo arquivo
        with open('insta.txt', 'w', encoding='utf-8') as output_file:
            for linha in linhas_filtradas:
                output_file.write(linha)
        
        print("Linhas filtradas foram salvas em 'insta.txt'.")
    
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chame a função com o caminho para o arquivo 'sucesso.txt'
filtrar_sucesso_ig('sucesso.txt')