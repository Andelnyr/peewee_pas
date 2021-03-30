from criar_base import Pessoa, Grupo, Nota

angelo = Pessoa(
    nome='Angelo',
    idade=18,
    senha='chupachupapassarinho',
    email='angelo@omundo.com'
)

angelo.save()
