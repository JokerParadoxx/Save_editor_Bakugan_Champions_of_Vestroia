import sys
from models import SaveDataModel
from views import MainView
from controllers import SaveEditorController


def main():
    """Punto de Entrada Principal (Bootstrap MVC)"""
    # 1. Instanciar el Modelo
    model = SaveDataModel()

    # 2. Instanciar la Vista
    view = MainView()

    # 3. Instanciar el Controlador (conecta Modelo y Vista)
    controller = SaveEditorController(model=model, view=view)

    # 4. Iniciar el bucle de eventos principal
    view.mainloop()


if __name__ == "__main__":
    main()
