import tkinter as tk

class GEBotInfoDisplay:
    __version__='1.1'
    """
    **GEBotInfoDisplay**
    
    A class for creating and updating a GUI display for GE Bot information using tkinter.

    Methods
    -------
    __init__() 
        Initializes the GEBotInfoDisplay object with the specified Tkinter root window.
        
        Parameters
        ----------
        root (tk.Tk)
            The Tkinter root window to which the display will be attached.
        Returns
        -------
        
    create_label()    
        Creates a labeled display area for a specific information category.
        
        Parameters
        ----------
        text : str 
            The label text.
        color : str
            The color of the label text.
        variable : tk.StringVar 
            The Tkinter StringVar associated with the displayed information.
        Returns
        -------
        
    update_info
        Updates the displayed information based on the provided status dictionary.
        Parameters
        ----------
        status_dic : dict 
            A dictionary containing information about GE Bot status.
        Returns
        -------
    
    """

    def __init__(self, root):
        """
        Initializes the GEBotInfoDisplay object with the specified Tkinter root window.
        
        Parameters
        ----------
        root (tk.Tk)
            The Tkinter root window to which the display will be attached.
        Returns
        -------
        """
        # create board
        self.root = root
        self.root.title("GEBot Info")
        self.root.geometry("400x100")
        self.root.configure(bg="#5F8A8B")

        # Initialize variables
        self.status = tk.StringVar()
        self.speed = tk.StringVar()
        self.expected_finish_time = tk.StringVar()
        self.remaining_images = tk.StringVar()
        self.time_elapsed = tk.StringVar()
        status_dic = {"status": "N/A",
                      "speed": "0",
                      "expected_finish_time": "0",
                      "remaining_images": "0",
                      "time_elapsed": "0"}
        self.update_info(status_dic)

        # Initialize board
        self.create_label("STATUS:", "yellow", self.status)
        self.create_label("Speed:", "purple", self.speed)
        self.create_label("Ex. FINISH:", "blue", self.expected_finish_time)
        self.create_label("T Elps:", "purple", self.time_elapsed)
        self.create_label("Pending:", "blue", self.remaining_images)

    def create_label(self, text, color, variable):
        """
        Creates a labeled display area for a specific information category.
        
        Parameters
        ----------
        text : str 
            The label text.
        color : str
            The color of the label text.
        variable : tk.StringVar 
            The Tkinter StringVar associated with the displayed information.
        Returns
        -------
        """
        frame = tk.Frame(self.root, bg="#5F8A8B")
        frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(frame, text=text, fg=color, font=('bold', 15), bg="#5F8A8B").pack(side=tk.LEFT)
        tk.Label(frame, textvariable=variable, fg=color, font=('bold', 15), bg="#5F8A8B").pack(side=tk.LEFT)

    def update_info(self, status_dic):
        """
        Updates the displayed information based on the provided status dictionary.
        Parameters
        ----------
        status_dic : dict 
            A dictionary containing information about GE Bot status.
        Returns
        -------
        """
        self.status.set(status_dic["status"])
        self.speed.set(status_dic["speed"])
        self.expected_finish_time.set(status_dic["expected_finish_time"])
        self.remaining_images.set(status_dic["remaining_images"])
        self.time_elapsed.set(status_dic["time_elapsed"])
    

    def __getattr__(self, attrib):
        if attrib=="__version__":
            return self.__version__
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attrib}'")

if __name__ == "__main__":
    root = tk.Tk()
    gebot_display = GEBotInfoDisplay(root)

    # Update information using the update_info method
    status_dic = {"status": "Running",
                  "speed": "15 MB/s",
                  "expected_finish_time": "2 hours",
                  "remaining_images": "50%",
                  "time_elapsed": "100"}
    gebot_display.update_info(status_dic=status_dic)

    root.mainloop()
