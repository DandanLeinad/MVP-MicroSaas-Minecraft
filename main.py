from backup import core, detect_bedrock, detect_java


def main():
    print("==== Minecraft Backup CLI ====")
    edition = input("Qual edição você usa? (java/bedrock): ").strip().lower()

    try:
        if edition == "java":
            worlds_path = detect_java.get_java_worlds_path()
        elif edition == "bedrock":
            worlds_path = detect_bedrock.get_bedrock_worlds_path()
        else:
            print("❌ Edição inválida. Digite 'java' ou 'bedrock'.")
            return
    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return

    core.menu(worlds_path)


if __name__ == "__main__":
    main()
