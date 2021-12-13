from enum import IntEnum, unique


@unique
class HttpStatusCode(IntEnum):

    """ Http Status Code Enum.
    source: https://pythonise.com/categories/python/http-status-code-enum
    """

    # INFORMATIONAL RESPONSES (100–199)
    CONTINUE = 100
    SWITCHING_PROTOCOL = 101
    PROCESSING = 102
    EARLY_HINTS = 103

    # SUCCESSFUL RESPONSES (200–299)
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # REDIRECTS (300–399)
    MULTIPLE_CHOICE = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    UNUSED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # status codes >= 400 are not used,
    # since they all will raise a HyplagRequestException
