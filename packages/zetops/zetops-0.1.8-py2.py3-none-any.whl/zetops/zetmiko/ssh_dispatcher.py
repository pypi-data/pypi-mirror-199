from netmiko.ssh_dispatcher import CLASS_MAPPER,platforms,platforms_str,\
    telnet_platforms_str,CLASS_MAPPER_BASE,FILE_TRANSFER_MAP
from zetops.zetmiko.huawei import HuaweiZetSSH
from zetops.zetmiko.hillstone import HillStoneSSH
from zetops.zetmiko.fiberhome import FiberHomeSSH
from zetops.zetmiko.mypower import MypowerOsSSH

CLASS_MAPPER['hillstone'] = HillStoneSSH
CLASS_MAPPER['huawei'] = HuaweiZetSSH
CLASS_MAPPER['fiberhome'] = FiberHomeSSH
CLASS_MAPPER['mypower'] = MypowerOsSSH

platforms = list(CLASS_MAPPER.keys())
platforms.sort()
platforms_base = list(CLASS_MAPPER_BASE.keys())
platforms_base.sort()
platforms_str = "\n".join(platforms_base)
platforms_str = "\n" + platforms_str

scp_platforms = list(FILE_TRANSFER_MAP.keys())
scp_platforms.sort()
scp_platforms_str = "\n".join(scp_platforms)
scp_platforms_str = "\n" + scp_platforms_str

telnet_platforms = [x for x in platforms if "telnet" in x]
telnet_platforms_str = "\n".join(telnet_platforms)
telnet_platforms_str = "\n" + telnet_platforms_str


def ConnectHandler(*args, **kwargs):
    """Factory function selects the proper class and creates object based on device_type."""
    device_type = kwargs["device_type"]
    if device_type not in platforms:
        if device_type is None:
            msg_str = platforms_str
        else:
            msg_str = telnet_platforms_str if "telnet" in device_type else platforms_str
        raise ValueError(
            "Unsupported 'device_type' "
            "currently supported platforms are: {}".format(msg_str)
        )
    ConnectionClass = ssh_dispatcher(device_type)
    return ConnectionClass(*args, **kwargs)


Netmiko = ConnectHandler
Zetmiko = ConnectHandler


def ssh_dispatcher(device_type):
    """Select the class to be instantiated based on vendor/platform."""
    return CLASS_MAPPER[device_type]
