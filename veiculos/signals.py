from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TipoCombustivel, Marca, TipoPropriedade


@receiver(post_migrate)
def cadastrar_marcas_padrao(sender, **kwargs):
    if sender.name != 'veiculos': 
        return
    
    marca_padrao = [
        "Ford", 
        "Fiat", 
        "Volkswagen", 
        "Audi",
        "Renault",
        "Volvo",
        "Citroën",
        "Chevrolet",
        "Mercedes-Benz",
        "Volare",
        "Iveco",
        "Mascarello",
        "New Holland",
        "Tramontini",
        "Caterpillar",
        "Case",
        "Valtra",
        "Toyota",
        "Honda",
        "Hyundai",
        "Kia",
        "Nissan",
        "Peugeot",
        "Mitsubishi",
        "Subaru",
        "Suzuki",
        "Mazda",
        "Chery",
        "JAC Motors",
        "BYD",
        "Great Wall",
        "Jeep",
        "Dodge",
        "Ram",
        "Chrysler",
        "Lexus",
        "Infiniti",
        "Acura",
        "Porsche",
        "Ferrari",
        "Lamborghini",
        "Maserati",
        "Bentley",
        "Rolls-Royce",
        "Bugatti",
        "Mini",
        "Land Rover",
        "Jaguar",
        "Alfa Romeo",
        "Opel",
        "Skoda",
        "Seat",
        "Tesla"
        ]
    
    for marca in marca_padrao:
        Marca.objects.get_or_create(marca=marca)
        print(f'Marca criada: {marca}')


@receiver(post_migrate)
def cadastrar_combustivel_padrao(sender, **kwargs):
    if sender.name != 'veiculos': 
        return
    
    combustivel_padrao = [
        "Gasolina", 
        "Etanol", 
        "Diesel", 
        ]
    
    for combustivel in combustivel_padrao:
        TipoCombustivel.objects.get_or_create(combustivel=combustivel)
        print(f'Marca criada: {combustivel}')


@receiver(post_migrate)
def cadastrar_propriedade_padrao(sender, **kwargs):
    if sender.name != 'veiculos': 
        return
    
    propriedade_padrao = [
        "Próprio", 
        "Terceiro", 
        ]
    
    for propriedade in propriedade_padrao:
        TipoPropriedade.objects.get_or_create(propriedade=propriedade)
        print(f'Marca criada: {propriedade}')
    