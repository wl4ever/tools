from NetworkManagement.Service.SegmentService import SegmentService
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Models.segment import Segment
from NetworkManagement.ping import PingTool

if __name__ == '__main__':
    netDevSvc = NetworkDeviceService()

    #segSvc = SegmentService()
    #seg_list = segSvc.getSegmentByZone('M')

    #location = 'sh'
    #
    #for seg in seg_list:
    #   print(seg.items())
    #   if seg.location != location:
    #       continue
    #   pt = PingTool(seg.segment+'/'+str(seg.mask))
    #   pt.probe().filter()
    #   reachable_ip_list = [ r[0] for r in pt.result ]
    #   for ip in reachable_ip_list:
    #       print(ip)
    #       d = xDevice(ip, zone=seg.role, location=seg.location, isICMPReachable=True)
    #       d.render()
    #       netDevSvc.save(d)

    #seg = Segment('10.20.101.0', role='JiaoYi', zone='M', location='sh')
    #pt = PingTool(seg.segment+'/'+str(seg.mask))
    #pt.probe().filter()
    #reachable_ip_list = [ r[0] for r in pt.result ]
    reachable_ip_list = [
'192.168.254.12',
'192.168.254.21',
'192.168.254.24',
'192.168.254.25',
'192.168.254.23',
'192.168.254.41',
'192.168.254.51',
'192.168.254.42'
    ]
    for ip in reachable_ip_list:
        print(ip)
        #d = xDevice(ip, zone=seg.role, location=seg.location, isICMPReachable=True)
        d = xDevice(ip, zone='DMZ', location='fz', isICMPReachable=True)
        d.render()
        print(d.items())
        netDevSvc.save(d)
        
