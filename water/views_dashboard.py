# water/views_dashboard.py
from django.views.generic import TemplateView
from django.db.models import F
from .models import Run

class LiveBoardView(TemplateView):
    template_name = 'dashboard/live.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        farms = farms_for_user(self.request.user)
        active = Run.objects.filter(ended_at__isnull=True, outlet__plot__zone__farm__in=farms) \
                            .select_related('outlet__plot__zone__farm')
        ctx['active_runs'] = active
        return ctx
