import smtplib
import datetime as dt
import json
from utils import CredentialManager

class SendEmail:
    __version__='1.1'
    """
    **SendEmail**
    
    A class to send email notifications when the GE bot process is stopped.


    Methods
    -------
    __init__()
        Initializes the SendEmail object.

        Parameters
        ----------
        config_path : str, optional 
            The path to the configuration file (default is './resources/config.json').
        credData : str, optional 
            The path to the credential data file (default is "./resources/cred.dat").
        
        Returns
        -------
        None

    process_stopped()
        Sends email notifications when the GE bot process is stopped.

        For each email ID in the configured list, connects to the SMTP server, logs in, and sends a notification email.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
    
    """

    def __init__(self, config_path='./resources/config.json', credData="./resources/cred.dat"):
        """
        Initializes the SendEmail object.

        Parameters
        ----------
        config_path : str, optional 
            The path to the configuration file (default is './resources/config.json').
        credData : str, optional 
            The path to the credential data file (default is "./resources/cred.dat").
        
        Returns
        -------
        None
        
        """
        with open(config_path) as file:
            self.config = json.load(file)
        self.emailIDs = self.config['emailID']
        self.machineID = self.config['machineID']

        cm = CredentialManager()
        self.aEmail, self.aPassword = cm.decrypt()

    def process_stopped(self):
        """
        Sends email notifications when the GE bot process is stopped.

        For each email ID in the configured list, connects to the SMTP server, logs in, and sends a notification email.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        for eID in self.emailIDs:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=self.aEmail, password=self.aPassword)
                connection.sendmail(from_addr=self.aEmail,
                                    to_addrs=eID,
                                    msg=f"Subject:GE-BOT email \n\n GE bot is stopped, Please check the Machine {self.machineID}"
                                    )
            print("{} Status email sent to {}".format(dt.datetime.now().replace(microsecond=0), eID))

        def __getattr__(self, attrib):
            if attrib=="__version__":
                return self.__version__
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attrib}'")



if __name__=="__main__":
    se = SendEmail()
    # se.process_stopped()
    print(se.__version__())



