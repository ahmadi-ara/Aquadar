from .models import Farm, Zone, Plot, Outlet, Waterman, Supervisor, Run
from django import forms
from django.contrib import admin


# ---------- Inlines ----------
class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 1


class PlotInline(admin.TabularInline):
    model = Plot
    extra = 1


class OutletInline(admin.TabularInline):
    model = Outlet
    extra = 1


# ---------- Farm ----------
@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [ZoneInline]


# ---------- Zone ----------
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "farm")
    list_filter = ("farm",)
    search_fields = ("name", "farm__name")
    inlines = [PlotInline]

# ---------- Plot ----------

class PlotAdminForm(forms.ModelForm):
    generate_outlets_count = forms.IntegerField(
        required=False,
        min_value=1,
        label="Generate outlets (1..n)",
        help_text="Enter a number to auto‑create outlets numbered 1 through n."
    )

    class Meta:
        model = Plot
        fields = "__all__"


@admin.register(Plot)   # ✅ decorate the ModelAdmin, not the form
class PlotAdmin(admin.ModelAdmin):
    form = PlotAdminForm
    list_display = ("name", "zone", "farm_name")
    list_filter = ("zone__farm", "zone")
    search_fields = ("name", "zone__name", "zone__farm__name")
    inlines = [OutletInline]

    def farm_name(self, obj):
        return obj.zone.farm.name
    farm_name.short_description = "Farm"

    def save_model(self, request, obj, form, change):
        # Save the plot itself first
        super().save_model(request, obj, form, change)

        # Check if user entered a number for auto‑generation
        n = form.cleaned_data.get("generate_outlets_count")
        if n:
            # Reset to exactly 1..n
            obj.outlets.all().delete()
            new_outlets = [Outlet(plot=obj, number=i) for i in range(1, n + 1)]
            Outlet.objects.bulk_create(new_outlets)


# ---------- Outlet ----------
@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ("number", "plot", "zone_name", "farm_name")
    list_filter = ("plot__zone__farm", "plot__zone")
    search_fields = ("plot__name", "plot__zone__name", "plot__zone__farm__name")

    def zone_name(self, obj):
        return obj.plot.zone.name
    zone_name.short_description = "Zone"

    def farm_name(self, obj):
        return obj.plot.zone.farm.name
    farm_name.short_description = "Farm"


# ---------- Supervisor ----------
@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active")
    filter_horizontal = ("farms",)
    list_filter = ("is_active",)
    search_fields = ("user__username",)


# ---------- Waterman ----------
@admin.register(Waterman)
class WatermanAdmin(admin.ModelAdmin):
    list_display = ("name", "farm", "is_active")
    list_filter = ("farm", "is_active")
    search_fields = ("name", "farm__name")


# ---------- Run ----------
@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = (
        "outlet",
        "plot_name",
        "zone_name",
        "farm_name",
        "started_at",
        "ended_at",
        "duration_seconds",
        "temperature_c",
        "is_anomalous_short",
        "is_anomalous_long",
    )
    list_filter = (
        "outlet__plot__zone__farm",
        "outlet__plot__zone",
        "outlet__plot",
        "is_anomalous_short",
        "is_anomalous_long",
    )
    search_fields = (
        "outlet__number",
        "outlet__plot__name",
        "outlet__plot__zone__name",
        "outlet__plot__zone__farm__name",
    )
    date_hierarchy = "started_at"

    def plot_name(self, obj):
        return obj.outlet.plot.name
    plot_name.short_description = "Plot"

    def zone_name(self, obj):
        return obj.outlet.plot.zone.name
    zone_name.short_description = "Zone"

    def farm_name(self, obj):
        return obj.outlet.plot.zone.farm.name
    farm_name.short_description = "Farm"
