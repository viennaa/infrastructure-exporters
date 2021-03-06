import exporter
import requests
from apic_exporters.apic_exporter import Apicexporter
from prometheus_client import Gauge

class Apichealth(Apicexporter):

    def __init__(self, exporterType, exporterConfig):
        super().__init__(exporterType, exporterConfig)
        self.gauge = {}
        self.gauge['network_apic_cpu_percentage'] = Gauge('network_apic_cpu_percentage',
                                                          'network_apic_cpu_percentage',
                                                          ['hostname'])
        self.gauge['network_apic_maxMemAlloc'] = Gauge('network_apic_maxMemAlloc',
                                                          'network_apic_maxMemAlloc',
                                                          ['hostname'])
        self.gauge['network_apic_memFree'] = Gauge('network_apic_memFree',
                                                          'network_apic_memFree',
                                                          ['hostname'])                                                 
                                    
    def collect(self):
        self.metric_count = 0
        self.apicHealthUrl =  "https://" + self.apicInfo['hostname'] + "/api/node/class/procEntity.json?"
        self.apicHealthInfo = self.apicGetRequest(self.apicHealthUrl, self.loginCookie, self.apicInfo['proxy'])
        self.apicMetrics = self.apicHealthInfo['imdata'][0]['procEntity']['attributes']
        if self.status_code == 200:
            self.metric_count = 3

    def export(self):
        if self.status_code == 200:
            self.gauge['network_apic_cpu_percentage'].labels(self.apicInfo['hostname']).set(self.apicMetrics['cpuPct'])
            self.gauge['network_apic_maxMemAlloc'].labels(self.apicInfo['hostname']).set(self.apicMetrics['maxMemAlloc'])
            self.gauge['network_apic_memFree'].labels(self.apicInfo['hostname']).set(self.apicMetrics['memFree'])                                                                                                  