from typing import List, Dict, Any
from src.models.car.car import Car
from src.models.personnel.driver import Driver

class TeamDatabase:
    """Hardcoded 2024 MVP Data containing all 10 F1 teams and 20 drivers."""
    
    @staticmethod
    def _create_car(downforce: int, drag: int, weight: int, tire: int, power: int, rel: int) -> Car:
        c = Car()
        c.aero.downforce = downforce; c.aero.drag_efficiency = drag
        c.chassis.weight_reduction = weight; c.chassis.tire_preservation = tire
        c.powertrain.power_output = power; c.powertrain.reliability = rel
        return c

    @staticmethod
    def get_initial_teams() -> Dict[str, Dict[str, Any]]:
        return {
            "Red Bull Racing": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(95, 95, 95, 90, 95, 90),
                "drivers": [
                    Driver("Max Verstappen", 55_000_000, rating=98, speed=99, consistency=98, tire_management=95),
                    Driver("Sergio Perez", 10_000_000, rating=85, speed=86, consistency=80, tire_management=89)
                ]
            },
            "Ferrari": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(92, 90, 88, 85, 94, 88),
                "drivers": [
                    Driver("Charles Leclerc", 34_000_000, rating=94, speed=97, consistency=88, tire_management=88),
                    Driver("Carlos Sainz", 12_000_000, rating=90, speed=90, consistency=92, tire_management=90)
                ]
            },
            "McLaren": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(94, 92, 90, 93, 93, 95),
                "drivers": [
                    Driver("Lando Norris", 20_000_000, rating=93, speed=95, consistency=93, tire_management=91),
                    Driver("Oscar Piastri", 8_000_000, rating=89, speed=92, consistency=88, tire_management=85)
                ]
            },
            "Mercedes": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(88, 93, 85, 88, 94, 96),
                "drivers": [
                    Driver("Lewis Hamilton", 45_000_000, rating=95, speed=94, consistency=96, tire_management=98),
                    Driver("George Russell", 18_000_000, rating=91, speed=92, consistency=90, tire_management=88)
                ]
            },
            "Aston Martin": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(85, 87, 82, 85, 93, 90),
                "drivers": [
                    Driver("Fernando Alonso", 18_000_000, rating=92, speed=90, consistency=95, tire_management=94),
                    Driver("Lance Stroll", 3_000_000, rating=81, speed=82, consistency=75, tire_management=80)
                ]
            },
            "Alpine": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(78, 80, 80, 80, 85, 88),
                "drivers": [
                    Driver("Pierre Gasly", 6_000_000, rating=86, speed=87, consistency=86, tire_management=84),
                    Driver("Esteban Ocon", 6_000_000, rating=86, speed=86, consistency=85, tire_management=86)
                ]
            },
            "Williams": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(75, 88, 75, 78, 93, 85),
                "drivers": [
                    Driver("Alex Albon", 3_000_000, rating=87, speed=89, consistency=85, tire_management=87),
                    Driver("Logan Sargeant", 1_000_000, rating=75, speed=76, consistency=70, tire_management=72)
                ]
            },
            "RB": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(80, 80, 80, 80, 95, 90),
                "drivers": [
                    Driver("Yuki Tsunoda", 2_000_000, rating=84, speed=87, consistency=78, tire_management=82),
                    Driver("Daniel Ricciardo", 2_000_000, rating=83, speed=84, consistency=83, tire_management=83)
                ]
            },
            "Sauber": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(70, 75, 75, 75, 85, 88),
                "drivers": [
                    Driver("Valtteri Bottas", 10_000_000, rating=86, speed=88, consistency=85, tire_management=84),
                    Driver("Zhou Guanyu", 2_000_000, rating=80, speed=81, consistency=83, tire_management=84)
                ]
            },
            "Haas": {
                "budget": 140_000_000,
                "car": TeamDatabase._create_car(82, 80, 78, 70, 88, 80),
                "drivers": [
                    Driver("Nico Hulkenberg", 2_000_000, rating=85, speed=88, consistency=84, tire_management=81),
                    Driver("Kevin Magnussen", 5_000_000, rating=82, speed=84, consistency=78, tire_management=80)
                ]
            }
        }
