from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from services.stats_services import StatsService
from decorators.decorators import roles_required

class StatsAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "admin")
    def get(self):
        claims = get_jwt()
        role = claims.get("role")

        stats = StatsService.get_stats_for_role(role)
        return stats, 200
