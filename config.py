import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
EMAIL_FROM        = os.environ.get("EMAIL_FROM")
EMAIL_PASSWORD    = os.environ.get("EMAIL_PASSWORD")
EMAIL_TO          = os.environ.get("EMAIL_TO")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
TOP_N     = 5

RSS_FEEDS = [
    # Open source news
    ("OMG Ubuntu",        "https://www.omgubuntu.co.uk/feed"),
    ("It's FOSS News",    "https://news.itsfoss.com/rss"),
    ("LWN.net",           "https://lwn.net/headlines/rss"),
    ("Linux Today",       "https://www.linuxtoday.com/feed/"),
    ("Phoronix",          "https://www.phoronix.com/rss.php"),
    ("GamingOnLinux",     "https://www.gamingonlinux.com/article_rss.php"),
    # Community
    ("r/opensource",      "https://www.reddit.com/r/opensource/.rss"),
    ("r/linux",           "https://www.reddit.com/r/linux/.rss"),
    ("r/selfhosted",      "https://www.reddit.com/r/selfhosted/.rss"),
    # Italiani
    ("Tom's Hardware IT", "https://www.tomshw.it/rss_news.xml"),
    ("Multiplayer.it",    "https://www.multiplayer.it/rss/news.xml"),
]

BOOST_KEYWORDS = [
    # Open source
    "open source", "opensource", "free software", "foss", "floss",
    "github", "gitlab", "released", "release", "version", "update",
    "rilasciato", "aggiornamento", "nuova versione",
    # Software rilevante
    "linux", "kernel", "mesa", "wayland", "pipewire",
    "firefox", "libreoffice", "blender", "gimp", "inkscape",
    "kde", "gnome", "gtk", "qt",
    "python", "rust", "go", "java",
    # Gaming open source
    "proton", "wine", "lutris", "steam",
    "godot", "openttd", "supertuxkart",
    # Self hosting
    "selfhosted", "self-hosted", "homelab", "nextcloud", "jellyfin",
]

PENALTY_KEYWORDS = [
    # Fuori tema
    "mobile", "ios", "android", "iphone", "samsung",
    "nft", "blockchain", "crypto", "metaverse", "web3",
    "playstation", "xbox", "nintendo",
    "dash cam", "smartwatch", "tablet",
    "amazon", "alibaba", "aliexpress",
    # Contenuti evergreen non news
    "how to install", "beginners guide", "what is",
    "come installare", "guida per principianti",
]
