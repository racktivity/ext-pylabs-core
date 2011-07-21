import unittest
from racktivity.common import convert
from racktivity.common.GUIDLoader import Value
class Converter(unittest.TestCase):
    
    
    def test_asciinr2int(self):
        valDef = Value(type="number", scale=3, min=100, max=2500, size=2)
        errocode, value = convert.ascii2emu("2405", valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, 2.405)
        errocode, value = convert.ascii2emu("2600", valDef)
        self.assertEqual(errocode, 12)
        errocode, value = convert.ascii2emu("50", valDef)
        self.assertEqual(errocode, 12)
    
    def test_asciibool2bool(self):
        valDef = Value(type="bool")
        errocode, value = convert.ascii2emu("0", valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, False)
        errocode, value = convert.ascii2emu("1", valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, True)
    
    def test_asciistring2string(self):
        valDef = Value(type="string", length=8)
        stringok = "12345678"
        longstring = "123456789"
        errocode, value = convert.ascii2emu(stringok, valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, stringok)
        errocode, value = convert.ascii2emu(longstring, valDef)
        self.assertEqual(errocode, 12)
    
    def test_asciiip2string(self):
        valDef = Value(type="IP")
        ip = "192.168.20.1"
        errocode, value = convert.ascii2emu(ip, valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, ip)
        invalidip = "13482394782"
        errocode, value = convert.ascii2emu(invalidip, valDef)
        self.assertEqual(errocode, 12)
        invalidip = "256.0.0.0"
        errocode, value = convert.ascii2emu(invalidip, valDef)
        self.assertEqual(errocode, 12)
        
    def test_asciimac2string(self):
        valDef = Value(type="mac")
        mac = "00:24:d6:8d:0c:82"
        errocode, value = convert.ascii2emu(mac, valDef)
        self.assertEqual(errocode, 0)
        self.assertEqual(value, mac)
        invalidmac = "13482394782"
        errocode, value = convert.ascii2emu(invalidmac, valDef)
        self.assertEqual(errocode, 12)
    
    def test_ascsii2readonly(self):
        for typ in ("version", "raw", "pointer"):
            valDef = Value(type=typ)
            errocode, value = convert.ascii2emu("3.5", valDef)
            self.assertEqual(errocode, 6)
    
    def test_ascsii_invalid_type(self):
        valDef = Value(type="invalid")
        errocode, value = convert.ascii2emu("3.5", valDef)
        self.assertEqual(errocode, 5)
    def test_int(self):
        self.assertEqual(convert.bin2int("\x03\x5A"), 23043)
        self.assertEqual(convert.bin2int("\x5A"), 90)
        self.assertEqual(convert.bin2int(convert.number2bin(23043, 2)), 23043)
    
    def test_string(self):
        data = "My string %$#@"
        databin = "My string %$#@\0%^&#*%^$*"
        res=  convert.string2bin(data, len(data)+5)
        self.assertEqual(res[0:-5], data)
        self.assertEqual(convert.bin2string(databin), data)
        self.assertEqual(convert.bin2string(data), data)
    
    def test_ip(self):
        data = "192.168.12.1"
        binip = "\xC0\xA8\x0C\x01"
        self.assertEqual(convert.ipaddress2bin(data), binip)
        self.assertEqual(convert.bin2ipaddress(binip), data)
    
    def test_mac(self):
        data = "00:24:d6:8d:0c:82"
        macbin = "\x00\x24\xd6\x8d\x0c\x82"
        self.assertEqual(convert.mac2bin(data), macbin)
        self.assertEqual(convert.bin2macaddress(macbin), data)
    
    def test_version(self):
        version = 3.5
        binversion = "\x03\x05"
        self.assertEqual(convert.version2bin(version), binversion)
        self.assertEqual(convert.bin2version(binversion), version)
        
    def test_bool(self):
        bintrue = "\x01"
        binfalse = "\x00"
        self.assertEqual(convert.bin2bool(bintrue), True)
        self.assertEqual(convert.bool2bin(True), bintrue)
        self.assertEqual(convert.bin2bool(binfalse), False)
        self.assertEqual(convert.bool2bin(False), binfalse)

if __name__ == '__main__':
    unittest.main()