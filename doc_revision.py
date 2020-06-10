## Questão 5 ##
# A interface State:
class State:
    def setDocument(self, document):
        self.document = document
    def render(self):
        pass
    def publish(self, msg):
        pass

# Os estados concretos:
class Draft(State):
    def render(self):
        print("Documento em rascunho")
    def publish(self, msg):
        if msg == "Published by user":
            self.document.changeState(Moderation())
        if msg == "Published by admin":
            self.document.changeState(Published())

class Moderation(State):
    def render(self):
        print("Documento em moderação")
    def publish(self, msg):
        if msg == "Review failed":
            self.document.changeState(Draft())
        if msg == "Approved by admin":
            self.document.changeState(Published())


class Published(State):
    def render(self):
        print("Documento publicado")
    def publish(self, msg):
        if msg == "Publication expired":
            self.document.changeState(Draft())

# A classe documento. As mudanças de contexto vão ser simuladas por mensagens nos métodos
# de 
class Document:
    def __init__(self, initialState):
        self.state = initialState
        self.state.setDocument(self)

    def changeState(self, newState):
        self.state = newState
        self.state.setDocument(self)

    def render(self):
        self.state.render()
        return self

    def publish(self, msg):
        self.state.publish(msg)
        return self

# O método publish simula todas as mudanças de contexto indiscriminadamente.
# Façamos instanciações de alguns exemplos

doc = Document(Draft())
doc.publish("Published by user").render().publish("Review failed")
doc.render().publish("Published by admin").render().publish("Publication expired")
doc.render().publish("Published by user").render().publish("Approved by admin").render()