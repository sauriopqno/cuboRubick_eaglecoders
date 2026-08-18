from collections import deque

class Cubo:
    pasos = {}
    padres = {}
    visitados = {}
    cola = deque()

    fin = [1, 2, 3, 4, 
             5, 6, 7, 8, 
             9, 10, 11, 12, 
             13, 14, 15, 16,
             17, 18, 19, 20, 
             21, 22, 23, 24]

    inicio = [22,9,13,11,10,12,19,7,1,3,5,24,23,4,21,8,2,6,17,15,18,16,20,14]

    movimientos = [
        [[13, 1],  [14, 2], [1,5], [2, 6], [5, 9],[6,10],[9,13], [10, 14], [ 23, 20], [20, 21], [21, 22], [22, 23]], # U'
        [[3, 0], [0, 1], [1, 2], [2, 3], [16, 6], [17, 7], [20, 12], [21, 13], [12, 16], [13, 17], [6, 20], [7, 21]],    # F'
        [[21,0],[22,1],[7,4],[4,5],[5,6],[6,7],[19,10],[16,11],[1,16],[0,19],[10,21],[11,22]],                         # R'
        [[5,1],[6,2],[9,5],[10,6],[13,9],[14,10],[1,13],[2,14],[21,20],[22,21],[23,22],[20,23]],                         # U
        [[1,0],[2,1],[3,2],[0,3],[20,6],[21,7],[16,12],[17,13],[6,16],[7,17],[12,20],[13,21]],                         # F
        [[19,0],[16,1],[5,4],[6,5],[7,6],[4,7],[21,10],[22,11],[11,16],[10,19],[0,21],[1,22]]                          # R
    ] 
    movimientosNombre = ["U'", "F'","R'","U","F","R"]
    movimientosNombreReverso = ["U", "F","R","U'","F'","R'"]

    movimientosActual = {}

    def solucion(self, actual):
        print(f"Cantidad de movimientos para resolver el cubo: {self.pasos[tuple(actual)]}")
        sol = []
        actual_tuple = tuple(actual)
        inicio_tuple = tuple(self.inicio)
        
        while actual_tuple != inicio_tuple:
            sol.append(self.movimientosActual[actual_tuple])
            actual_tuple = tuple(self.padres[actual_tuple])
            
        for i in sol:
            print("mov reverso", self.movimientosNombreReverso[self.movimientosNombre.index(i)])
        for i in sol[::-1]:
            print("mov", i, end=" ")
        print()

    def verificarFinal(self, actual):
        for i in range(6):
            caras = actual[i*4 : (i*4)+4]
            if max(caras) - min(caras) != 3:
                return False
        return True

    def BFS(self): 
        inicio_tuple = tuple(self.inicio)
        
        # Verificación por si el inicio ya es el estado final
        if self.verificarFinal(self.inicio):
            self.pasos[inicio_tuple] = 0
            return self.solucion(self.inicio)

        self.visitados[inicio_tuple] = True
        self.padres[inicio_tuple] = self.inicio
        self.pasos[inicio_tuple] = 0
        self.cola.append(self.inicio)

        while len(self.cola) > 0:
            actual = self.cola.popleft()
            actual_tuple = tuple(actual)

            # Generamos los movimientos
            for i in range(len(self.movimientos)):
                hijo = actual[:]
                for j in self.movimientos[i]:
                    hijo[j[1]] = actual[j[0]]
                
                hijo_tuple = tuple(hijo)
                
                if hijo_tuple not in self.visitados:
                    self.visitados[hijo_tuple] = True
                    self.padres[hijo_tuple] = actual
                    self.pasos[hijo_tuple] = self.pasos[actual_tuple] + 1
                    self.movimientosActual[hijo_tuple] = self.movimientosNombre[i]
                    
                    # Verificación temprana del estado objetivo
                    if self.verificarFinal(hijo):
                        return self.solucion(hijo)

                    self.cola.append(hijo)

        self.solucion(self.inicio)

if __name__ == "__main__":
    c = Cubo()
    c.BFS()
