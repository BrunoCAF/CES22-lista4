## Questão 2 ##

class PizzaComponent:
    def getDescricao(self):
        return self.__class__.__name__
    
    def getCustoTotal(self):
        return self.__class__.custo
        # O custo não é definido para classes abstratas

# O primeiro componente concreto é a massa
class Massa(PizzaComponent):
    custo = 1.0

# Criamos o decorator
class Decorator(PizzaComponent):
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente

    def getCustoTotal(self):
        return self.ingrediente.getCustoTotal() + PizzaComponent.getCustoTotal(self)

    def getDescricao(self):
        return self.ingrediente.getDescricao() + " com " + PizzaComponent.getDescricao(self)

# Agora criamos diversos componentes concretos para decorar nossas pizzas:
class Mussarela(Decorator):
    custo = 3.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

class Calabresa(Decorator):
    custo = 4.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

class Peperoni(Decorator):
    custo = 7.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

class Frango(Decorator):
    custo = 4.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

class Bacon(Decorator):
    custo = 5.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

class Presunto(Decorator):
    custo = 3.0
    def __init__(self, ingrediente):
        Decorator.__init__(self, ingrediente)

# Agora instanciamos alguns exemplos:
pizzaFrango = Frango(Mussarela(Massa()))
pizzaCalabresa = Calabresa(Mussarela(Massa()))
pizzaCalabresaPaulista = Calabresa(Massa())
melhorPizza = Peperoni(Mussarela(Massa()))

pizzas = [pizzaFrango, pizzaCalabresa, pizzaCalabresaPaulista, melhorPizza]
for pizza in pizzas:
    print(pizza.getDescricao() + ": R$ " + str(pizza.getCustoTotal()))



