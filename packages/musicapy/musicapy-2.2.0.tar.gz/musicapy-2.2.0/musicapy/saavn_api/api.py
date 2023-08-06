from . import services, utils


class SaavnAPI(services.SearchService, services.SongService, services.AlbumService, services.PlaylistService, utils.Utils):
    ''' :class:`SaavnAPI` class inherits all the services of the JioSaavn API
    used to search, get details and lyrics of songs and album'''
    pass
