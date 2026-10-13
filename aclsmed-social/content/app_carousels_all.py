"""Every app carousel, in posting order: Oct 14–16 (app_carousels.py), today's extra and Oct 17–31 (one file per app)."""
from content.app_carousels import APP_CAROUSELS as FIRST
from content.app_carousels_ac import AC_CAROUSELS
from content.app_carousels_cl import CL_CAROUSELS
from content.app_carousels_eb import EB_CAROUSELS

APP_CAROUSELS = sorted(FIRST + AC_CAROUSELS + CL_CAROUSELS + EB_CAROUSELS, key=lambda c: (c["date"], c["time"]))
