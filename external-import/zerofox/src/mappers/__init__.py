from typing import Any

from zerofox.app.endpoints import CTIEndpoint

from mappers.c2DomainsToInfrastructure import c2_domains_to_infrastructure
from mappers.exploitToTool import exploit_to_tool
from mappers.malwareToMalware import malware_to_malware
from mappers.phishingToInfrastructure import phishing_to_infrastructure
from mappers.ransomwareToMalware import ransomware_to_malware


def threat_feed_to_stix(feed: Any):
    return {
        CTIEndpoint.C2Domains: c2_domains_to_infrastructure,
        CTIEndpoint.Malware: malware_to_malware,
        CTIEndpoint.Ransomware: ransomware_to_malware,
        CTIEndpoint.Exploits: exploit_to_tool,
        CTIEndpoint.Phishing: phishing_to_infrastructure,
    }.get(feed)