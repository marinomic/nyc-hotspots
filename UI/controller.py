import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceLocation = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._provSelected = None

    def handleCreaGrafo(self, e):
        if self._provSelected is None:
            warnings.warn("Provider non selezionato")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Provider non selezionato"))
            self._view.update_page()
            return
        soglia = self._view._txtInDistanza.value
        if soglia is None or soglia == "":
            warnings.warn("Distanza non selezionata")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non selezionata"))
            self._view.update_page()
            return
        try:
            sogliaFloat = float(soglia)
        except ValueError:
            warnings.warn("Distanza non valida")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non valida"))
            self._view.update_page()
            return
        self._model.creaGrafo(self._provSelected, sogliaFloat)
        numNodes, numEdges = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato"))
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {numNodes}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero archi: {numEdges}"))
        self.fillDDTarget()
        self._view.update_page()

    def handleAnalizzaGrafo(self, e):
        nNodes, nEdges = self._model.getGraphDetails()
        if nNodes == 0 and nEdges == 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Grafo vuoto"))
            self._view.update_page()
            return
        lista = self._model.getNodesMostVicini()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Nodi con più vicini"))
        for node in lista:
            self._view._txt_result.controls.append(ft.Text(f"{node[0]} - {node[1]} vicini"))
        self._view.update_page()

    def handleCalcolaPercorso(self, e):
        target = self._choiceLocation
        substring = self._view._txtInString.value

        if substring == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, stringa non inserita."))
            self._view.update_page()
            return

        path, source = self._model.getCammino(target, substring)

        if path == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Non ho trovato un cammino fra {source} e {target}"))
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Ho trovato un cammino fra {source} e {target}:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()


    def fillDDProvider(self):
            allProviders = self._model.getProviders()

            # Metodo 1:
            # for p in allProviders:
            #     self._view._ddProvider.options.append(ft.dropdown.Option(text=p,
            #                                                              data=p,
            #                                                              on_click=self._view._controller.readDDProvider))
            # Metodo 2:
            providersDD = map(lambda p: ft.dropdown.Option(text=p, data=p, on_click=self._view._controller.readDDProvider),
                              allProviders)
            self._view._ddProvider.options.extend(providersDD)

            self._view.update_page()

    def readDDProvider(self, e):
        if e.control.data is None or e.control.data == "":
            self._provSelected = None
        else:
            self._provSelected = e.control.data
        print(f"Provider selected: {self._provSelected}")

    def fillDDTarget(self):
        locations = self._model._grafo.nodes
        targetsDD = map(lambda p: ft.dropdown.Option(text=p.Location, data=p, on_click=self._view._controller.readDDTarget),
                        locations)
        self._view._ddTarget.options.extend(targetsDD)
        self._view.update_page()

    def readDDTarget(self, e):
        if e.control.data is None or e.control.data == "":
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data
        print(f"Target selected: {self._provSelected}")
