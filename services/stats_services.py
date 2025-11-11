from repository.stats_repository import StatsRepository

class StatsService:
    @staticmethod
    def get_general_stats():
        """Métricas disponibles para moderadores y admins"""
        return {
            "total_users": StatsRepository.count_users(),
            "total_posts": StatsRepository.count_posts(),
            "total_comments": StatsRepository.count_comments(),
        }

    @staticmethod
    def get_admin_only_stats():
        """Métricas solo para admin"""
        return {
            "posts_last_week": StatsRepository.count_posts_last_week(),
            "comments_last_week": StatsRepository.count_comments_last_week(),
        }

    @staticmethod
    def get_stats_for_role(role):
        """Combina según el rol del usuario"""
        stats = StatsService.get_general_stats()
        if role == "admin":
            stats.update(StatsService.get_admin_only_stats())
        return stats