from enum import Enum


class Endpoints(str, Enum):
    PALADINS = "https://api.paladins.com/paladinsapi.svc"
    REALM_ROYALE = "https://api.realmroyale.com/realmapi.svc"
    SMITE = "https://api.smitegame.com/smiteapi.svc"
    STATUS_PAGE = "https://stk4xr7r1y0r.statuspage.io"  # http://status.hirezstudios.com
