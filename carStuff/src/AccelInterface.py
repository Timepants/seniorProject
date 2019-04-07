import smbus2 as smbus
import math

class AccelInterface(object): 
    # Register
    def __init__(self):
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
        self.address = 0x68
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
    
    def read_byte(self, reg):
        return self.bus.read_byte_data(self.address, reg)
    
    def read_word(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value
    
    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    
    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))
    
    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)
    
    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def getGyroX(self):
        return self.read_word_2c(0x43)
    
    def getGyroY(self):
        return self.read_word_2c(0x45)

    def getGyroZ(self):
        return self.read_word_2c(0x47)

    def getGyroXScaled(self):
        return self.getGyroX() / 131
    
    def getGyroYScaled(self):
        return self.getGyroY() / 131

    def getGyroZScaled(self):
        return self.getGyroZ() / 131
    
    def getAccelX(self):
        return self.read_word_2c(0x3b)

    def getAccelY(self):
        return self.read_word_2c(0x3d)

    def getAccelZ(self):
        return self.read_word_2c(0x3f)
    
    def getAccelXScaled(self):
        return self.getAccelX() / 16384.0

    def getAccelYScaled(self):
        return self.getAccelY() / 16384.0

    def getAccelZScaled(self):
        return self.getAccelZ() / 16384.0
    
    def getXRotation(self):
        return self.get_x_rotation(self.getAccelXScaled(), self.getAccelYScaled(), self.getAccelZScaled())
    
    def getYRotation(self):
        return self.get_y_rotation(self.getAccelXScaled(), self.getAccelYScaled(), self.getAccelZScaled())
