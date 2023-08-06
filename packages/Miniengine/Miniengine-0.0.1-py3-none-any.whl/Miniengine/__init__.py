import pygame
import math


class Tela():
    def __init__(self, largura, altura, titulo, tick=60, speed=1):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.tick = tick
        self.speed = speed
        self.dt = 1/tick*speed
        pygame.init()
        self.tela = pygame.display.set_mode((largura, altura))
    def desenhar(self, objeto):
        self.tela.blit(objeto.corpo, objeto.posicao)

    
class Objeto(pygame.Surface):
    def __init__(self, altura, largura, posicao, peso, velocidade, direcao, cor, tela, gravidade=False):
        self.altura = altura
        self.largura = largura
        self.posicao = posicao
        self.peso = peso
        self.velocidade = velocidade
        self.direcao = direcao
        self.tela = tela
        """self.dt = 1/tick*speed
        self.tick = tick"""
        if cor == "vermelho":
            cor = (255, 0, 0)
        elif cor == "azul":
            cor = (0, 0, 255)
        elif cor == "verde":
            cor = (0, 255, 0)
        elif cor == "amarelo":
            cor = (255, 255, 0)
        elif cor == "preto":
            cor = (0, 0, 0)
        elif cor == "branco":
            cor = (255, 255, 255)
        elif cor == "roxo":
            cor = (255, 0, 255)
        elif cor == "laranja":
            cor = (255, 165, 0)
        elif cor == "cinza":
            cor = (128, 128, 128)
        elif cor == "marrom":
            cor = (165, 42, 42)
        elif cor == "rosa":
            cor = (255, 192, 203)
        elif cor == "roxo claro":
            cor = (128, 0, 128)
        elif cor == "azul claro":
            cor = (0, 255, 255)
        elif cor == "verde claro":
            cor = (0, 255, 0)
        elif cor == "vermelho claro":
            cor = (255, 0, 0)
        elif cor == "amarelo claro":
            cor = (255, 255, 0)
        elif cor == "rosa claro":
            cor = (255, 192, 203)
        elif cor == "marrom claro":
            cor = (210, 105, 30)
        elif cor == "laranja claro":
            cor = (255, 165, 0)
        elif cor == "cinza claro":
            cor = (211, 211, 211)
        elif cor == "cinza":
            cor = (169, 169, 169)
        self.corpo = pygame.Surface((self.largura, self.altura))
        self.corpo.fill(cor)

    def atualizarPos(self, dt, gravidade=False):
        x, y = self.posicao
        self.dt = dt
        radians = math.radians(self.direcao)
        dx = self.velocidade * math.cos(radians)
        dy = self.velocidade * math.sin(radians)
        g = 9.8  # acceleration due to gravity in m/s²
        if gravidade:
            direction_rad = math.radians(self.direcao)

            current_speed_x = self.velocidade * math.cos(direction_rad)
            current_speed_y = self.velocidade * math.sin(direction_rad)

            # Add the specified speed to the y-axis
            new_speed_y = current_speed_y + 9.8 * dt

            # Calculate the new speed and direction
            new_speed = math.sqrt(current_speed_x ** 2 + new_speed_y ** 2)
            new_direction = math.degrees(math.atan2(new_speed_y, current_speed_x))

            # Update the object's speed and direction
            self.velocidade = new_speed
            self.direcao = new_direction
        new_x = x + dx * dt
        new_y = y + dy * dt
        self.posicao = (new_x, new_y)
    def ChecarColidir(self, objeto):
        if self.posicao[0] + self.largura > objeto.posicao[0] and self.posicao[0] < objeto.posicao[0] + objeto.largura:
            if self.posicao[1] + self.altura > objeto.posicao[1] and self.posicao[1] < objeto.posicao[1] + objeto.altura:
                return True
            else:
                return False
        else:
            return False
    def acelerar(self, dV, angulo):
        direcaoRad = math.radians(self.direcao)

        # Calculate the object's current x and y velocity components
        velocidadeX = self.velocidade * math.cos(direcaoRad)
        velocidadeY = self.velocidade * math.sin(direcaoRad)

        # Calculate the x and y components of the speed_change
        DeltaVX = dV * math.cos(angulo)
        DeltaVY = dV * math.sin(angulo)

        # Add the speed_change components to the current speed components
        VeloNovaX = velocidadeX + DeltaVX
        VeloNovaY = velocidadeY + DeltaVY

        # Calculate the new speed and direction
        velocidadeNova = math.sqrt(VeloNovaX ** 2 + VeloNovaY ** 2)
        direcaoNova = math.degrees(math.atan2(VeloNovaY, VeloNovaX))

        # Update the object's speed and direction
        self.velocidade = velocidadeNova
        self.direcao = direcaoNova

    def gravitar(self, object2, dt, g=0, distancia = False):
        cG = 6.67430 * (10 ** -11)
        dx = object2.posicao[0] - self.posicao[0]
        dy = object2.posicao[1] - self.posicao[1]
        angle1 = math.atan2(dy, dx)
        angle2 = math.atan2(-dy, -dx)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if g == 0:
            # Calculate the gravitational force
            force = cG * self.peso * object2.peso / (distance ** 2)

            # Calculate the acceleration due to gravity for both objects
            acceleration1 = (force / self.peso)*10000000000000
            acceleration2 = (force / object2.peso)*10000000000000

            # Determine the direction of the gravitational force for each object
        elif distancia == True:
            acceleration1 = g/((distance**2)/10000)
            acceleration2 = g/((distance**2)/10000)
        else:
            # If g is specified, use it as the acceleration due to gravity
            acceleration1 = g
            acceleration2 = g
        # Update the speed and direction of both objects based on the time interval dt
        self.acelerar(acceleration1 * dt, angle1)
        object2.acelerar(acceleration2 * dt, angle2)
def distancia(objeto1, objeto2):
    x1, y1 = objeto1.posicao
    x2, y2 = objeto2.posicao
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)
def Colide(object1, object2, COR=1):
    x1, y1 = object1.posicao
    x2, y2 = object2.posicao
    v1 = object1.velocidade
    v2 = object2.velocidade
    d1 = object1.direcao
    d2 = object2.direcao
    m1 = object1.peso
    m2 = object2.peso

    # Convert direction to radians
    r1 = math.radians(d1)
    r2 = math.radians(d2)

    # Calculate the normal vector (unit vector) between the two objects
    delta_x = x2 - x1
    delta_y = y2 - y1
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    normal_x = delta_x / distance
    normal_y = delta_y / distance

    # Calculate the relative velocity along the normal vector
    relative_velocity_x = v2 * math.cos(r2) - v1 * math.cos(r1)
    relative_velocity_y = v2 * math.sin(r2) - v1 * math.sin(r1)
    relative_velocity = relative_velocity_x * normal_x + relative_velocity_y * normal_y

    # Calculate the impulse using the COR
    impulse = 2 * relative_velocity * COR / (1/m1 + 1/m2)

    # Calculate the final velocities using the impulse
    if COR != 0:
        v1fx = v1 * math.cos(r1) + (impulse * normal_x) / m1
        v1fy = v1 * math.sin(r1) + (impulse * normal_y) / m1
        v2fx = v2 * math.cos(r2) - (impulse * normal_x) / m2
        v2fy = v2 * math.sin(r2) - (impulse * normal_y) / m2
    else:
        # In the case of COR = 0 (perfectly inelastic collision), objects stick together
        v1fx = (m1 * v1 * math.cos(r1) + m2 * v2 * math.cos(r2)) / (m1 + m2)
        v1fy = (m1 * v1 * math.sin(r1) + m2 * v2 * math.sin(r2)) / (m1 + m2)
        v2fx = v1fx
        v2fy = v1fy

    # Calculate the magnitudes and directions of the final velocities
    v1f = math.sqrt(v1fx ** 2 + v1fy ** 2)
    v2f = math.sqrt(v2fx ** 2 + v2fy ** 2)
    d1f = math.degrees(math.atan2(v1fy, v1fx))
    d2f = math.degrees(math.atan2(v2fy, v2fx))

    # Update the velocities and directions of the objects
    object1.velocidade = v1f
    object1.direcao = d1f
    object2.velocidade = v2f
    object2.direcao = d2f
    return object1, object2
    
