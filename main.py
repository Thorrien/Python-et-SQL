from app.controllers.login import Login
import sentry_sdk
from cle import CLE

def main():
    sentry_sdk.init(
        dsn=CLE,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True
    )
    loggin = Login()
    loggin.login()


if __name__ == "__main__":
    main()
    
