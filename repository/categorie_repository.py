from models.models import Categoria, db

class CategoriaRepository:
    @staticmethod
    def get_all():
        return Categoria.query.all()

    @staticmethod
    def get_by_id(id):
        return Categoria.query.get_or_404(id)

    @staticmethod
    def get_by_name(name):
        return Categoria.query.filter_by(name=name).first()

    @staticmethod
    def create(name):
        categoria = Categoria(name=name)
        db.session.add(categoria)
        db.session.commit()
        return categoria

    @staticmethod
    def update(categoria, name):
        categoria.name = name
        db.session.commit()
        return categoria

    @staticmethod
    def delete(categoria):
        db.session.delete(categoria)
        db.session.commit()