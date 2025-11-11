# services/categoria_service.py
from repository.categorie_repository import CategoriaRepository
from marshmallow import ValidationError

class CategoriaService:
    @staticmethod
    def list_all():
        return CategoriaRepository.get_all()

    @staticmethod
    def create(data):
        name = data.get("name", "").strip()
        if not name:
            raise ValidationError({"name": "El nombre no puede estar vacío"})
        if CategoriaRepository.get_by_name(name):
            raise ValidationError({"name": "Ya existe una categoría con ese nombre"})
        return CategoriaRepository.create(name)

    @staticmethod
    def update(id, data):
        categoria = CategoriaRepository.get_by_id(id)
        name = data.get("name", "").strip()
        if not name:
            raise ValidationError({"name": "El nombre no puede estar vacío"})
        existente = CategoriaRepository.get_by_name(name)
        if existente and existente.id != id:
            raise ValidationError({"name": "Ya existe otra categoría con ese nombre"})
        return CategoriaRepository.update(categoria, name)

    @staticmethod
    def delete(id):
        categoria = CategoriaRepository.get_by_id(id)
        CategoriaRepository.delete(categoria)
        return {"message": "Categoría eliminada correctamente"}
