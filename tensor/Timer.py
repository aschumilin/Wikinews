import time as SysTime 

class Timer(object):
    """Simple time measuring device."""
    """KEYWORDS: object-oriented, Time, TimeStringFormat"""
    
#    start = 0.0
#    end = 0.0
#    counting = False
    
    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.counting = False

   
        
    def click(self):
        if self.counting: 
            # end time measurement
            self.counting = False
            self.end = SysTime.time()
        else: 
            # begin time measurement
            self.counting = True
            self.start = SysTime.time()

            
            
    def show(self):
        if self.counting == True:
            return "started at: " + SysTime.strftime(" %H:%M:%S (%a, %d %b %Y)", SysTime.localtime(self.start))
        else:
            return str(self.end - self.start) + "s"
        
        
    def __str__(self):
        return self.show()
