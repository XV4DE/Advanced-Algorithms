import math


class Particle:
    def __init__(self, _mass: float = 1, _position: float = 0, _velocity: float = 0):
        self.mass = _mass
        self.position = _position
        self.velocity = _velocity

    def distance(self, other):
        return other.position - self.position

    def kinetic_energy(self):
        return 0.5 * self.velocity**2


class Universe:
    def __init__(self, _mass: Particle, _massless: Particle, _time: float = 0):
        self.mass = _mass
        self.massless = _massless
        self.time = _time
        self.G = 1

    def kinetic_energy(self):
        return self.massless.kinetic_energy()

    def potential_energy(self):
        return self.mass.mass * self.G/abs(self.mass.distance(self.massless))

    def time_to_get_to(self, xf):
        return ((xf - self.massless.position)/self.massless.velocity +
                self.mass.mass/(self.massless.position * abs(self.massless.position)) - self.mass.mass/(xf*abs(xf)))


