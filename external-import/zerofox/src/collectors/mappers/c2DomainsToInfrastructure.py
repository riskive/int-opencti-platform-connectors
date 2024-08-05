import ipaddress
from typing import List, Tuple, Union

from stix2 import Infrastructure, IPv4Address, IPv6Address, Relationship, Software
from zerofox.domain.c2Domains import C2Domain


def c2_domains_to_infrastructure(
    now: str, entry: C2Domain
) -> List[Union[Infrastructure, Relationship, IPv4Address, IPv6Address]]:
    """
    Creates a STIX Infrastructure/command-and-conrtol object from a ZeroFOX C2Domain object, along with
        - A set of IPAddress observables on each of the IP addresses associated with the C2 domain
    """
    entry_tags = entry.tags
    tags, tags_obtained_observables = _parse_tag_observables(entry_tags)

    infrastructure = Infrastructure(
        name=f"{entry.domain}",
        labels=tags,
        created=now,
        first_seen=entry.created_at,
        modified=entry.updated_at,
        infrastructure_types="command-and-control",
    )

    tag_observables_relationships = _get_observables_relationships(
        entry, infrastructure, tags_obtained_observables
    )
    ip_addresses = (
        [build_ip_stix_object(ip) for ip in entry.ip_addresses]
        if entry.ip_addresses
        else []
    )
    c2_ip_relationships = [
        Relationship(
            source_ref=infrastructure.id,
            target_ref=ip.id,
            relationship_type="consists-of",
            start_time=entry.created_at,
        )
        for ip in ip_addresses
    ]

    return (
        [infrastructure]
        + ip_addresses
        + c2_ip_relationships
        + tags_obtained_observables
        + tag_observables_relationships
    )


def _parse_tag_observables(tags: List[str]) -> Tuple[List[str], List[Software]]:
    observables = []
    non_parsed_tags = []
    for tag in tags:
        if tag.startswith("sample_type:"):
            observables.append(
                Software(
                    name=tag.replace("sample_type:", ""),
                )
            )
        else:
            non_parsed_tags.append(tag)
    return non_parsed_tags, observables


def _get_observables_relationships(
    entry: C2Domain, infra: Infrastructure, observables: List[Software]
) -> List[Relationship]:
    return [
        Relationship(
            source_ref=infra.id,
            target_ref=observable.id,
            relationship_type="consists-of",
            start_time=entry.created_at,
        )
        for observable in observables
    ]


def build_ip_stix_object(ip):
    version = ipaddress.ip_address(ip).version
    if version == 4:
        return IPv4Address(value=ip)
    elif version == 6:
        return IPv6Address(value=ip)
    else:
        raise ValueError(f"Invalid IP address: {ip}")
