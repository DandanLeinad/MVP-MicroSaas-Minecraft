from backup import core, detect_bedrock, detect_java


def run_cli():
    print("==== Minecraft Backup CLI ====")
    edition = input("Qual edição você usa? (java/bedrock): ").strip().lower()

    if edition == "java":
        path = detect_java.get_java_worlds_path()
    elif edition == "bedrock":
        path = detect_bedrock.get_bedrock_worlds_path()
    else:
        print("Edição inválida.")
        return

    if not path:
        print(
            "❌ Caminho não encontrado. O Minecraft pode não estar instalado."
        )
        return

    core.menu(path)
