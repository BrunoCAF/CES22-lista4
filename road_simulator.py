## Questão 1 ##
# Criamos uma interface para o motor
class Motor:
    def getName(self):
        return self.__class__.__name__

# Criamos a abstração veículo, que irá ser agregada de uma Motor abstrato
class Veiculo:
    def __init__(self, motor):
        self.motorizacao = motor

    def getName(self):
        return self.__class__.__name__ + " com " + self.motorizacao.getName()

    def getDescricao(self):
        return self.getName()

# A seguir criamos implementações concretas para os tipos de motor
class MotorEletrico(Motor):
    def __init__(self):
        self.bateria = 0.00

    def getBateria(self):
        return self.bateria

    def carregaBateria(self):
        self.bateria = max(1.00, self.bateria+1)

class MotorDeCombustao(Motor):
    capacidadeTanque = 100
    def __init__(self):
        self.volumeTanque = 0.00

    def getVolumeTanque(self):
        return self.volumeTanque

    def encheTanque(self, litros):
        self.volumeTanque = max(MotorDeCombustao.capacidadeTanque, self.volumeTanque+litros)

# Tomamos a liberdade de criar uma hierarquia de classes entre as implementações de motor
class MotorHibrido(MotorEletrico, MotorDeCombustao):
    def __init__(self):
        super(MotorEletrico, self)
        super(MotorDeCombustao, self)

# A seguir criamos classes derivadas do veículo, as quais não precisam se preocupar com 
# a relação de agregação com o motor, pois esta já é herdada da classe abstrata Veiculo
class Caminhao(Veiculo):
    peso = 10*1e3
    def __init__(self, motor, carga):
        super().__init__(motor)
        self.carga = carga
    
    def getDescricao(self):
        return self.getName() + "\nCarga: " + self.carga + "\nPeso: " + str(self.peso)

class Carro(Veiculo):
    peso = 1e3
    def getDescricao(self):
        return self.getName() + "\nPeso: " + str(self.peso)

class Onibus(Veiculo):
    peso = 3*1e3
    def __init__(self, motor, qtdPassageiros):
        super().__init__(motor)
        self.qtdPassageiros = qtdPassageiros

    def getDescricao(self):
        return self.getName() + "\nQuantidade de Passageiros: " + str(self.qtdPassageiros) + "\nPeso: " + str(self.peso)

## Questão 3 ##
# Criamos a fábrica abstrata de veículos, que irá produzir 3 produtos: 
# carros, caminhões e ônibus.
class AbstractFactory:
    def criarCarro(self):
        raise NotImplementedError
    def criarCaminhao(self, carga):
        raise NotImplementedError
    def criarOnibus(self, qtdPassageiros):
        raise NotImplementedError

# Cada um desses produtos pode vir com 3 tipos de motorização diferentes, donde teremos
# 3 fábricas concretas
class EletricoFactory(AbstractFactory):
    @classmethod
    def criarCarro(cls):
        return Carro(MotorEletrico())
    
    @classmethod
    def criarCaminhao(cls, carga):
        return Caminhao(MotorEletrico(), carga)
    
    @classmethod
    def criarOnibus(cls, qtdPassageiros):
        return Onibus(MotorEletrico(), qtdPassageiros)

class CombustaoFactory(AbstractFactory):
    @classmethod
    def criarCarro(cls):
        return Carro(MotorDeCombustao())
    
    @classmethod
    def criarCaminhao(cls, carga):
        return Caminhao(MotorDeCombustao(), carga)
    
    @classmethod
    def criarOnibus(cls, qtdPassageiros):
        return Onibus(MotorDeCombustao(), qtdPassageiros)

class HibridoFactory(AbstractFactory):
    @classmethod
    def criarCarro(cls):
        return Carro(MotorHibrido())
    
    @classmethod
    def criarCaminhao(cls, carga):
        return Caminhao(MotorHibrido(), carga)
    
    @classmethod
    def criarOnibus(cls, qtdPassageiros):
        return Onibus(MotorHibrido(), qtdPassageiros)

# Agora instanciamos alguns exemplos:
carroEletrico = EletricoFactory.criarCarro()
caminhaoCombustao = CombustaoFactory.criarCaminhao("Minério de Ferro")
onibusHibrido = HibridoFactory.criarOnibus(50)

veiculos = [carroEletrico, caminhaoCombustao, onibusHibrido]

for v in veiculos:
    print(v.getDescricao())