import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillDDLocalization(self):
        localizations=self._model.getAllLocalizations()
        localizationsDD=list(map(lambda x: ft.dropdown.Option(x), localizations))
        self._view.dd_localization.options=localizationsDD


    def handle_graph(self, e):
        self._model.buildGraph(self._view.dd_localization.value)
        n,m=self._model.getGraphDetails()
        archi=self._model.getAllEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {n} nodi e {m} archi."))
        for a in archi:
            self._view.txt_result.controls.append(ft.Text(f'{a[0]} <-> {a[1]} : peso {a[2]["weight"]}'))


        self._view.update_page()


    def analyze_graph(self, e):
        componenti_conn=self._model.getInfoConnessa()
        for c in componenti_conn:
            nodi=",".join(str(n.GeneID) for n in c[0])
            self._view.txt_result.controls.append(ft.Text(f'{nodi} | dimensione componente= {c[1]}'))
        self._view.update_page()


    def handle_path(self, e):
        path=self._model.getBestPath()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'La lunghezza del cammino trovato è {len(path)}.'))
        self._view.txt_result.controls.append(ft.Text(f'Il cammino trovato è il seguente: '))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()


